from dataclasses import dataclass


@dataclass
class Function:
    name: str
    qualified_name: str
    file: str
    line: int
    end_line: int

@dataclass
class Class:
    name: str
    qualified_name: str
    file: str
    line: int
    end_line: int


@dataclass
class Method:
    name: str
    class_name: str
    class_qualified_name: str
    qualified_name: str
    file: str
    line: int
    end_line: int

@dataclass
class Import:
    module: str
    name: str
    file: str
    line: int

@dataclass
class AnalyzedFile:
    path: str
    functions: list[Function]
    classes: list[Class]
    methods: list[Method]
    imports: list[Import]

@dataclass
class Relationship:
    source: str
    type: str
    target: str
    file: str
    line: int

@dataclass
class RepositoryAnalysis:
    files: list[AnalyzedFile]
    relationships: list[Relationship]

@dataclass
class GraphNode:
    id: str
    type: str
    name: str
    file: str | None
    line: int | None
    end_line: int | None


@dataclass
class RepositoryGraph:
    nodes: dict[str, GraphNode]
    relationships: list[Relationship]

@dataclass
class EvidenceItem:
    type: str
    content: str
    file: str
    start_line: int | None
    end_line: int | None
    symbol: str | None


@dataclass
class EvidenceBundle:
    items: list[EvidenceItem]

@dataclass
class SemanticDocument:
    node_id: str
    text: str

@dataclass
class RetrievedCandidate:
    node: GraphNode
    score: float

@dataclass
class AssemblyContext:
    candidate_nodes: list[GraphNode]
    graph: RepositoryGraph
    repository_path: str