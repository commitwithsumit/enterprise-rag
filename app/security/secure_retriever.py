from app.query.analyzer import analyze_query
from app.query.router import route_query

from app.retrieval.document_retriever import search_documents
from app.retrieval.structured_retriever import search_structured_data
from app.retrieval.json_retriever import search_json_logs

from app.security.resource_access import ResourceAccessService


class SecureRetriever:

    def __init__(self):

        self.access_service = ResourceAccessService()

    def retrieve(
        self,
        query: str,
        user,
        user_roles,
        user_permissions,
        required_permission: str,
        top_k: int = 3,
    ):

        analysis = analyze_query(query)

        sources = route_query(analysis)

        authorized_resource_ids = (
            self.access_service
            .get_authorized_resource_ids(
                user=user,
                user_roles=user_roles,
                user_permissions=user_permissions,
                required_permission=required_permission,
            )
        )

        print("\nSECURITY CHECK")
        print("----------------")
        print("User:", user.username)
        print(
            "Authorized resources:",
            authorized_resource_ids
        )

        results = []

        if "DOCUMENT" in sources:

            document_results = search_documents(
                query,
                k=top_k,
                allowed_resource_ids=authorized_resource_ids,
            )

            for result in document_results:

                resource_id = result.metadata.get(
                    "resource_id"
                )

                if resource_id in authorized_resource_ids:

                    results.append(result)

        if "STRUCTURED" in sources:

            structured_results = search_structured_data(
                query,
                allowed_resource_ids=authorized_resource_ids,
            )

            for result in structured_results:

                resource_id = (
                    result.metadata.get("resource_id")
                )

                if resource_id in authorized_resource_ids:

                    results.append(result)

        if "JSON_LOG" in sources:

            json_results = search_json_logs(
                query,
                allowed_resource_ids=authorized_resource_ids,
            )

            for result in json_results:

                resource_id = (
                    result.metadata.get("resource_id")
                )

                if resource_id in authorized_resource_ids:

                    results.append(result)

        return results