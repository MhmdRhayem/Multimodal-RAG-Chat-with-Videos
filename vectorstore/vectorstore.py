from langchain_core.embeddings import Embeddings
from langchain_community.vectorstores.lancedb import LanceDB
from typing import Any, Optional

class MultimodalLanceDB(LanceDB):
    def __init__(
        self,
        connection=None,
        embedding=None,
        uri="./lancedb",
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
