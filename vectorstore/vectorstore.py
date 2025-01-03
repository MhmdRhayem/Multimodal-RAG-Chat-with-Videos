from langchain_core.embeddings import Embeddings
from langchain_community.vectorstores.lancedb import LanceDB
from typing import Any, Optional, List

class MultimodalLanceDB(LanceDB):
    def __init__(
        self,
        connection=None,
        embedding=None,
        uri="./vectorstore/lancedb",
        vector_key="vector",
        id_key="id",
        text_key="text",
        image_path_key="extracted_frame_path",
        table_name="MULTIRAGTABLE",
        api_key=None,
        region=None,
        mode="append",
    ):
        super(MultimodalLanceDB, self).__init__(
            connection,
            embedding,
            uri,
            vector_key,
            id_key,
            text_key,
            table_name,
            api_key,
            region,
            mode,
        )
        self._image_path_key = image_path_key

    def add_text_image_pairs(
        self,
        texts,
        image_paths,
        metadatas=None,
        ids=None,
        **kwargs: Any,
    ):
        assert len(texts) == len(image_paths), "the len of transcripts should be equal to the len of images"
        docs = []
        embeddings = self._embedding.embed_image_text_pairs(texts=list(texts), images=list(image_paths))
        for idx, text in enumerate(texts):
            embedding = embeddings[idx]
            metadata = metadatas[idx] if metadatas else {"video_segment_id": idx}
            docs.append(
                {
                    self._vector_key: embedding,
                    self._id_key: idx,
                    self._text_key: text,
                    self._image_path_key: image_paths[idx],
                    "metadata": metadata,
                }
            )
        if "mode" in kwargs:
            mode = kwargs["mode"]
        else:
            mode = self.mode
        if self._table_name in self._connection.table_names():
            tbl = self._connection.open_table(self._table_name)
            if self.api_key is None:
                tbl.add(docs, mode=mode)
            else:
                tbl.add(docs)
        else:
            self._connection.create_table(self._table_name, data=docs)
        return ids

    @classmethod
    def from_text_image_pairs(
        cls,
        texts: List[str],
        image_paths: List[str],
        embedding: Embeddings,
        metadatas: Optional[List[dict]] = None,
        connection: Any = None,
        vector_key: Optional[str] = "vector",
        id_key: Optional[str] = "id",
        text_key: Optional[str] = "text",
        image_path_key: Optional[str] = "extracted_frame_path",
        table_name: Optional[str] = "MULTIRAGTABLE",
        **kwargs: Any,
    ):

        instance = MultimodalLanceDB(
            connection=connection,
            embedding=embedding,
            vector_key=vector_key,
            id_key=id_key,
            text_key=text_key,
            image_path_key=image_path_key,
            table_name=table_name,
        )
        instance.add_text_image_pairs(texts, image_paths, metadatas=metadatas, **kwargs)

        return instance