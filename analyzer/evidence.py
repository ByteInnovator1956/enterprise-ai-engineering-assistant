from analyzer.models import (
    EvidenceItem,
    EvidenceBundle,
    Relationship,
)


# build_source_evidence()


# build_relationship_evidence()


def build_evidence_bundle(
    items: list[EvidenceItem],
) -> EvidenceBundle:
    return EvidenceBundle(
        items=items
    )


def build_source_evidence(
    file_path,
    symbol,
    start_line,
    end_line,
):
    with open(file_path, "r") as file:
        lines = file.readlines()

    content = "".join(
        lines[start_line - 1:end_line]
    )

    return EvidenceItem(
        type="source",
        content=content,
        file=file_path,
        start_line=start_line,
        end_line=end_line,
        symbol=symbol,
    )


def build_relationship_evidence(relationship):
    content = (
        f"{relationship.source} "
        f"{relationship.type} "
        f"{relationship.target}"
    )

    return EvidenceItem(
        type="relationship",
        content=content,
        file=relationship.file,
        start_line=relationship.line,
        end_line=relationship.line,
        symbol=relationship.source,
    )

def build_test_evidence(
    file_path,
    symbol,
    start_line,
    end_line,
):
    with open(file_path, "r") as file:
        lines = file.readlines()

    content = "".join(
        lines[start_line - 1:end_line]
    )

    return EvidenceItem(
        type="test",
        content=content,
        file=file_path,
        start_line=start_line,
        end_line=end_line,
        symbol=symbol,
    )

def build_documentation_evidence(
    file_path,
    start_line,
    end_line,
):
    with open(file_path, "r") as file:
        lines = file.readlines()

    content = "".join(
        lines[start_line - 1:end_line]
    )

    return EvidenceItem(
        type="documentation",
        content=content,
        file=file_path,
        start_line=start_line,
        end_line=end_line,
        symbol=None,
    )