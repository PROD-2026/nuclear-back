import os
import re

from pathspec import GitIgnoreSpec

from src.domain.vaule_objects.vulnerability import Vulnerability, VulnerabilitySeverity
from src.ports.compression import ICompressionProvider
from src.ports.ml import IMLProvider
from src.ports.storage import IStorageProvider


class ScannerService:
    def __init__(
        self,
        storage_provider: IStorageProvider,
        compression_provider: ICompressionProvider,
        ml_provider: IMLProvider,
        secrets_patterns: list[str],
    ) -> None:
        self.pattern = re.compile(
            "|".join(f"({pattern})" for pattern in secrets_patterns)
        )

        self._storage = storage_provider
        self._compression = compression_provider
        self._ml = ml_provider

    async def found_vulnerabilities(
        self,
        report_id: str,
        whitelist: list[str] | None = None,
        blacklist: list[str] | None = None,
    ) -> list[Vulnerability]:
        whitelist = whitelist or []
        blacklist = blacklist or []

        archive_data = await self._storage.read(f"{report_id}.zip")
        project_path = await self._compression.unarchive(
            data=archive_data, out_path=report_id, type="zip"
        )

        rules = ["!" + line for line in whitelist] + blacklist

        spec = GitIgnoreSpec.from_lines(rules)
        files = set(spec.match_tree_files(project_path, negate=True))

        vulnerabilities = []
        for file in files:
            try:
                lines = await self._storage.read_lines(os.path.join(project_path, file))
            except:
                continue

            for i, line in enumerate(lines):
                found = self.pattern.finditer(line)
                vulnerabilities += [
                    Vulnerability(
                        file=file,
                        line=i,
                        masked_value=str(vul.string),
                        pattern=str(self.pattern),
                        severity=VulnerabilitySeverity.LOW,
                    )
                    for vul in found
                ]

        await self._storage.delete(f"{report_id}.zip")

        return vulnerabilities

    async def check_by_ml(
        self, vulnerabilities: list[Vulnerability]
    ) -> list[Vulnerability]:
        ml_answer = await self._ml.check_vulnerabilities(
            values=[vuln.masked_value for vuln in vulnerabilities]
        )

        res = []
        for i, vuln_info in enumerate(ml_answer):
            original_vuln = vulnerabilities[i]
            if not vuln_info.is_vulnerability:
                continue

            res.append(
                Vulnerability(
                    file=original_vuln.file,
                    line=original_vuln.line,
                    masked_value=original_vuln.masked_value,
                    pattern=original_vuln.pattern,
                    severity=vuln_info.severity,
                )
            )

        return res
