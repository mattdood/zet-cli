from pathlib import Path
from typing import List, Union

from ein.edge import Edge
from ein.graph import Graph
from ein.node import Node

from .repo import Repo
from .settings import Settings
from .zet import Zet

settings = Settings()


class Db:
    """Database representations of each zet.

    This stores a searchable representation of the categories,
    tags, and other metadata associated with each note file.
    Synchronizing the DB is recommended if anything has changed
    in the DB other than additions to a repo.

    The DB will always store **all** zets from every repo, ensuring
    that every note is available for linking and searching.
    """

    def __init__(self) -> None:
        """The DB is a file stored in the environment path."""
        self.db_path = Path(settings.install_path / ".env/zets.db")
        self.db = Graph(db_path=self.db_path.as_posix())

    def sync_db(self) -> None:
        """Synchronize the DB with fresh data.

        Creates a new database that has all data from every
        repository. The zets are converted to nodes based on their
        metadata and the links within each zet are converted to edges
        to connect nodes.

        Calling this is best used when the repos have had some updates
        separate from just additions. The database doesn't support updates
        or deletions to avoid complexity. It's often easier to just recreate
        the DB from scratch.
        """
        # removes current DB path then recreates it
        # this is to start fresh on any new data that was
        # added to the DB or changed
        if self.db_path.exists():
            self.db_path.unlink()
            self.db = Graph(db_path=self.db_path.as_posix())

        # all repos
        repos = [Repo(repo_path) for repo_path in settings.get_repo_paths()]

        # all zets
        zets =  []
        for repo in repos:
            nodes = []
            edges = []
            zets += [Zet(zet_path) for zet_path in repo.list_zets(full_path=True)]
            nodes.append([self._construct_node(zet) for zet in zets])
            edges += [self._construct_edges(zet) for zet in zets]

            self.db.add_nodes(schema_name=repo.repo_name, nodes=nodes)
            self.db.add_edges(schema_name=repo.repo_name, edges=edges)

    def _construct_node(self, zet: Zet) -> Node:
        """Node constructor for the graph database.

        Params:
            zet (Zet): A Zet to construct a node.

        Returns:
            node (Node): A node representation of a zet.
        """

        # links don't need to be in Node obj.
        zet.metadata.pop("links", None)
        return Node(schema_name=zet.repo_name, id=zet.path, body=zet.metadata)

    def _construct_edges(self, zet: Zet) -> Union[List[Edge], List]:
        """Edge constructor for the graph database.

        Params:
            zet (Zet): A Zet to construct edges for. Each link in the
                zet will be a separate edge.

        Returns:
            edges (Union[List[Edge], List]): A list of edges to add
                or an empty list.
        """
        edges = []

        # source node links
        links = zet.metadata.pop("links", None)
        if links:
            source_node_body = zet.metadata
            source_node = Node(schema_name=zet.repo_name, id=zet.path, body=source_node_body)

            for link in links:
                target_zet = Zet(path=link)

                # don't need links
                target_zet.metadata.pop("links", None)

                target_node_body = target_zet.metadata
                target_node = Node(schema_name=target_zet.repo_name, id=target_zet.path, body=target_node_body)
                edges.append(Edge(schema_name=source_node.schema_name, source=source_node, target=target_node))
        return edges

    def add_zet(self) -> None:
        pass

