from langchain_google_vertexai import ChatVertexAI
import streamlit as st
import os

os.environ["GOOGLE_API_KEY"] = st.secrets["GOOGLE_API_KEY"]

#llm = ChatVertexAI(model="gemini-1.5-pro")
llm = ChatVertexAI(model="gemini-1.5-pro:generateContent")

#####################################################
from langchain_core.tools import tool
from langchain_core.pydantic_v1 import BaseModel, Field
import requests

def requestGet(api_key: str, bt: str, resourceId: str):
    """Retrieve data from an API using REST GET."""
    response = requests.get(
        f"https://freki-staging.tinvio.dev/api/v1/{bt}/{resourceId}",
        headers={"API_KEY": api_key},
    )
    return response.json()

def requestList(api_key: str, bt: str):
    """Retrieve a list of data from an API using REST GET."""
    response = requests.get(
        f"https://freki-staging.tinvio.dev/api/v1/{bt}",
        headers={"API_KEY": api_key},
    )
    return response.json()

def requestPost(api_key: str, bt: str, payload: str):
    """Retrieve data from an API using REST POST with payload."""
    print(f"requestPayload: {payload}")
    response = requests.post(
        f"https://freki-staging.tinvio.dev/api/v1/{bt}",
        headers={"API_KEY": api_key},
        json=payload,
    )
    return response.json()

class ListChartOfAccounts(BaseModel):
    """Retrieves a JSON array of objects. Each object is a Chart of Account.

    Example JSON Response (delimiters are ###)
    ###
    [
        {
            "accountClass": "Asset",
            "accountType": "Current Asset",
            "resourceId": "e91ae7de-9893-4dad-a95a-d2d5251b4dcc"
        }
    ]
    ###
    """

class ListTaxProfiles(BaseModel):
    """Retrieves a JSON array of objects. Each object is a Tax Profile.

    Example JSON Response (delimiters are ###)
    ###
    [
        {
            "name": "Exempt Export",
            "description": null,
            "status": "ACTIVE",
            "vatType": "PERCENTAGE",
            "vatValue": 0,
            "isDefault": true,
            "isShipping": false,
            "organizationResourceId": "73cecab1-6680-4f84-83db-3843fa148380",
            "resourceId": "1958df31-78fe-4c8c-82dc-991c55f39641"
        }
    ]
    ###
    """

class ListJournals(BaseModel):
    """Retrieves a JSON array of objects. Each object is a Journal.

    Example JSON Response (delimiters are ###)
    ###
    [
        {
            "resourceId": "e0dfc6e0-ed26-4a2b-9b22-42fcf3c47ee6",
            "reference": "api test 51",
            "status": "ACTIVE",
            "tags": [
                "test"
            ],
            "valueDate": 1679987272000,
            "totalCreditAmount": 10,
            "totalDebitAmount": 10,
            "contactResourceId": null,
            "internalNotes": null,
            "taxInclusion": false,
            "taxVatApplicable": false,
            "type": "JOURNAL_CASHFLOW",
            "crossCurrency": false,
            "currencyCode": "SGD",
            "currencySymbol": "S$",
            "subTotalCredit": 10,
            "subTotalDebit": 10,
            "totalCreditVat": 0,
            "totalDebitVat": 0,
            "journalEntries": [
                {
                    "creditAmount": null,
                    "creditTaxVat": 0,
                    "currencyCode": "SGD",
                    "currencySymbol": "S$",
                    "crossCurrency": false,
                    "debitAmount": 10,
                    "description": null,
                    "journalResourceId": null,
                    "organizationAccountResourceId": "816032c4-315a-40a9-b245-1723d8021431",
                    "resourceId": "89ad4db0-b258-468a-a002-97a73bf10713",
                    "rateFunctionalToSource": null,
                    "rateSourceToFunctional": 1,
                    "taxProfileResourceId": null
                },
                {
                    "creditAmount": 10,
                    "creditTaxVat": 0,
                    "currencyCode": "SGD",
                    "currencySymbol": "S$",
                    "crossCurrency": false,
                    "debitAmount": null,
                    "description": null,
                    "journalResourceId": null,
                    "organizationAccountResourceId": "816032c4-315a-40a9-b245-1723d8021431",
                    "resourceId": "ff5d7926-1aeb-4005-8ac5-b97079b6ab6a",
                    "rateFunctionalToSource": null,
                    "rateSourceToFunctional": 1,
                    "taxProfileResourceId": null
                }
            ]
        }
    ]
    ###
    """

class ListContacts(BaseModel):
    """Retrieves a JSON array of objects. Each object is a Contact.

    Example JSON Response (delimiters are ###)
    ###
    [{"name": "John", "email": "john@example.com", "contactResourceId": "33988ec3-708f-48ad-bccb-6bbbd40d5127"}]
    ###
    """

class ListInvoices(BaseModel):
    """Retrives a JSON array of objects. Each object is an Invoice.

    Example JSON Response (delimiters are ###)
    ###
    [
    {
    "data": {
        "totalWithHold": null,
        "valueDate": 1699640400000,
        "billFrom": {
            "name": "Juan_Ortega_Org_SG",
            "taxId": null,
            "addresses": [
                {
                    "addressLine1": "test",
                    "addressLine2": "",
                    "addressType": "BILLING",
                    "city": "singapore",
                    "country": "SG",
                    "postalCode": "12345",
                    "state": "singapore"
                }
            ]
        },
        "billTo": null,
        "shipping": null,
        "contactResourceId": null,
        "terms": 0,
        "internalNotes": null,
        "invoiceNotes": null,
        "resourceId": "d2273efd-4698-4feb-9627-9010c59d91ae",
        "isTaxVATApplicable": false,
        "taxInclusion": false,
        "settings": {
            "itemTax": null
        },
        "status": "DRAFT",
        "dueDate": 1699640400000,
        "subTotal": 80,
        "totalShipping": 0,
        "totalVat": 0,
        "reference": "ai test 3",
        "totalAmount": 80,
        "currencyCode": "SGD",
        "currencySymbol": "S$",
        "tags": null,
        "paymentRecords": [],
        "attachments": [],
        "lineItems": [
            {
                "discount": {
                    "rateType": "FLAT",
                    "rateValue": 0
                },
                "name": "papaya",
                "quantity": 10,
                "organizationAccountResourceId": null,
                "unit": "",
                "unitPrice": 2,
                "resourceId": "534a79a1-cfda-414f-b640-5760f7d3456d",
                "itemResourceId": null,
                "taxProfile": null
            },
            {
                "discount": {
                    "rateType": "FLAT",
                    "rateValue": 0
                },
                "name": "oranges",
                "quantity": 20,
                "organizationAccountResourceId": null,
                "unit": "",
                "unitPrice": 3,
                "resourceId": "16dac8b9-9494-4ab6-96e4-3b38efcde1a2",
                "itemResourceId": null,
                "taxProfile": null
            }
        ]
    }
    ]
    ###
    """

class ListBills(BaseModel):
    """Retrives a JSON array of objects. Each object is an Bill.

    Example JSON Response (delimiters are ###)
    ###
    [
     {
        "isTaxWithholdApplicable": null,
        "settings": {
            "itemTax": null
        },
        "reference": "api test 22",
        "dueDate": 1784749751000,
        "taxInclusion": false,
        "contactResourceId": "f5f54b02-9a7a-4859-8f80-5eadb26db5d5",
        "terms": 30,
        "internalNotes": null,
        "resourceId": "405cbdd1-0547-4cb3-966d-57d4c3f46b20",
        "vatSupplierFxRate": null,
        "valueDate": 1684749751000,
        "status": "DRAFT",
        "isTaxVATApplicable": false,
        "currencySymbol": "S$",
        "currencyCode": "SGD",
        "subTotal": 0,
        "totalVat": 0,
        "totalAmount": 0,
        "totalWithHold": null,
        "paymentRecords": [],
        "lineItems": [
            {
                "discount": {
                    "rateType": "FLAT",
                    "rateValue": 0
                },
                "name": "someitem",
                "quantity": 1,
                "organizationAccountResourceId": null,
                "taxProfile": null,
                "unit": "",
                "unitPrice": 0,
                "resourceId": "d3b95410-7a5a-4547-bdca-a16ef2d81232",
                "itemResourceId": null
            }
        ]
    ]
    ###
    """

class GetBill(BaseModel):
    """Retrieves a JSON object. The object is Bill data.

    Example of a successful JSON response (delimiters are ###)
    ###
    {
    "data": {
        "isTaxWithholdApplicable": null,
        "settings": {
            "itemTax": null
        },
        "reference": "api test 22",
        "dueDate": 1784749751000,
        "taxInclusion": false,
        "contactResourceId": "f5f54b02-9a7a-4859-8f80-5eadb26db5d5",
        "terms": 30,
        "internalNotes": null,
        "resourceId": "405cbdd1-0547-4cb3-966d-57d4c3f46b20",
        "vatSupplierFxRate": null,
        "valueDate": 1684749751000,
        "status": "DRAFT",
        "isTaxVATApplicable": false,
        "currencySymbol": "S$",
        "currencyCode": "SGD",
        "subTotal": 0,
        "totalVat": 0,
        "totalAmount": 0,
        "totalWithHold": null,
        "paymentRecords": [],
        "lineItems": [
            {
                "discount": {
                    "rateType": "FLAT",
                    "rateValue": 0
                },
                "name": "someitem",
                "quantity": 1,
                "organizationAccountResourceId": null,
                "taxProfile": null,
                "unit": "",
                "unitPrice": 0,
                "resourceId": "d3b95410-7a5a-4547-bdca-a16ef2d81232",
                "itemResourceId": null
            }
        ],
        "attachments": [],
        "tags": []
      }
    }
    ###

    Example of a failed JSON response (delimiters are ###)
    ###
    {
    "error": {
        "error_type": "not_found",
        "errors": [
            "Bill not found"
        ]
      }
    }
    ###
    """

class GetInvoice(BaseModel):
    """Retrieves a JSON object. The object is Invoice data.

    Example of a successful JSON response (delimiters are ###)
    ###
    {
    "data": {
        "totalWithHold": null,
        "valueDate": 1699640400000,
        "billFrom": {
            "name": "Juan_Ortega_Org_SG",
            "taxId": null,
            "addresses": [
                {
                    "addressLine1": "test",
                    "addressLine2": "",
                    "addressType": "BILLING",
                    "city": "singapore",
                    "country": "SG",
                    "postalCode": "12345",
                    "state": "singapore"
                }
            ]
        },
        "billTo": null,
        "shipping": null,
        "contactResourceId": null,
        "terms": 0,
        "internalNotes": null,
        "invoiceNotes": null,
        "resourceId": "d2273efd-4698-4feb-9627-9010c59d91ae",
        "isTaxVATApplicable": false,
        "taxInclusion": false,
        "settings": {
            "itemTax": null
        },
        "status": "DRAFT",
        "dueDate": 1699640400000,
        "subTotal": 80,
        "totalShipping": 0,
        "totalVat": 0,
        "reference": "ai test 3",
        "totalAmount": 80,
        "currencyCode": "SGD",
        "currencySymbol": "S$",
        "tags": null,
        "paymentRecords": [],
        "attachments": [],
        "lineItems": [
            {
                "discount": {
                    "rateType": "FLAT",
                    "rateValue": 0
                },
                "name": "papaya",
                "quantity": 10,
                "organizationAccountResourceId": null,
                "unit": "",
                "unitPrice": 2,
                "resourceId": "534a79a1-cfda-414f-b640-5760f7d3456d",
                "itemResourceId": null,
                "taxProfile": null
            },
            {
                "discount": {
                    "rateType": "FLAT",
                    "rateValue": 0
                },
                "name": "oranges",
                "quantity": 20,
                "organizationAccountResourceId": null,
                "unit": "",
                "unitPrice": 3,
                "resourceId": "16dac8b9-9494-4ab6-96e4-3b38efcde1a2",
                "itemResourceId": null,
                "taxProfile": null
            }
        ]
    }
    ###

    Example of a failed JSON response (delimiters are ###)
    ###
    {
    "error": {
        "error_type": "not_found",
        "errors": [
            "Invoice not found"
        ]
      }
    }
    ###
}
    
    """
    resourceId: str = Field(..., description="Invoice Resource Id, string format")

class CreateBTLineItem(BaseModel):
    """Define a Line Item JSON structure.

    Example (delimiters are ###)
    ###
        {
            "discount": 7.0,
            "name": "First Item",
            "quantity": 1,
            "accountResourceId": "7ffd2f3e-3bc0-4a74-bade-7724041a92fd",
            "taxProfileResourceId": "452bbcdc-4108-44fd-b0a4-d84db53c716e",
            "unit": "dollars",
            "unitPrice": 10.0,

        }
    ###
    """
    discount: float = Field(None, description="Line item discount, float format")
    name: str = Field(..., description="Line item name, string format")
    unit: str = Field(None, description="Line item unit, string format")
    unitPrice: float = Field(None, description="Line item unit price, float format")
    quantity: float = Field(None, description="Line item quantity, float format")
    accountResourceId: str = Field(None, description="Line item chart of account resourceId, type uuidv4")
    taxProfileResourceId: str = Field(None, description="Line item tax profile resourceId, type uuidv4")

class CreateInvoice(BaseModel):
    """Create an Invoice.

    If successful please respond with the reference.

    Example (delimiters are ###)
    ###
    {
    "reference": "api test 47",
    "valueDate": 1685509673000,
    "contactResourceId": "81f0534a-78d4-4c9f-825d-c9c29f761e52",
    "terms": 60,
    "internalNotes": "foo",
    "invoiceNotes": "bar",
    "lineItems": [
        {
            "name": "First Item",
            "quantity": 1,
            "unit": "dollars",
            "unitPrice": 10.0
        },
        {
            "name": "Second Item",
            "quantity": 1,
            "unit": "dollars",
            "unitPrice": 10.0
        }
    ],
    "saveAsDraft": true
    }
    ###
    """
    reference: str = Field(..., description="Invoice reference, string format")
    valueDate: int = Field(..., description="Invoice value Date in epoch milliseconds integer format")
    tags: list[str] = Field(None, description="Invoice tags, array of strings format")
    terms: int = Field(None, description="Invoice tags, must be one: 0,7,15,30,45,60")
    invoiceNotes: str = Field(None, description="Invoice notes, string format")
    internalNotes: str = Field(None, description="Invoice internal notes, string format")
    lineItems: list[CreateBTLineItem] = Field(None, description="Invoice Line Items, array of objects format")
    saveAsDraft: bool = Field(..., description="Save the Invoice as a draft?, this is mandatory and required, default is true, boolean type")
    contactResourceId: str = Field(None, description="The contact resource id, uuidv4 format type")


class CreateJournalEntry(BaseModel):
    """Define Journal Entry JSON schema.

    Lookup the accountResourceId by retrieving the list of chart of accounts using the 'ListChartOfAccounts' function.
    Lookup the taxProfileResourceId by retriving the list of tax profiles using the 'ListTaxProfiles' function.

    Example (delimiters are ###)
    ###
        {
            "accountResourceId": "610a9b0f-9117-4f0b-a5c2-f34013c76c5a",
            "description": "something",
            "amount": 10.0,
            "type": "DEBIT",
            "taxProfileResourceId": "48d34c6b-1b20-4a6a-a366-3d380a1679e9",
            "exchangeRate": 0.8
        }
    ###
    """
    accountResourceId: str = Field(..., description="Journal Entry accountResourceId, this is mandatory field, uuidv4 format")
    description: str = Field(None, description="Journal Entry description, string format")
    amount: float = Field(..., description="Journal Entry amount, this is mandatory field, float format")
    type: str = Field(..., description="Journal Entry type, this is mandatory field, can be: CREDIT or DEBIT, string format")
    exchangeRate: float = Field(None, description="Journal Entry exchange rate, float format")
    taxProfileResourceId: str = Field(None, description="Journal Entry taxResourceId, uuidv4 format")

class CreateJournal(BaseModel):
    """Create a Journal.

    If successful please respond with the reference.

    Example (delimiters are ###)
    ###
    {
    "reference": "api test 65",
    "valueDate": 1679987272000,
    "saveAsDraft": true,
    "journalEntries": [
        {
            "accountResourceId": "610a9b0f-9117-4f0b-a5c2-f34013c76c5a",
            "amount": 10.0,
            "type": "DEBIT",
            "taxProfileResourceId": "48d34c6b-1b20-4a6a-a366-3d380a1679e9",
            "exchangeRate": 0.8
        },{
            "accountResourceId": "610a9b0f-9117-4f0b-a5c2-f34013c76c5a",
            "amount": 10.0,
            "type": "CREDIT",
            "taxProfileResourceId": "48d34c6b-1b20-4a6a-a366-3d380a1679e9"
        }
    ],
    "taxInclusion": false,
    "taxVatApplicable": true
    }
    ###
    """
    reference: str = Field(..., description="Invoice reference, string format")
    valueDate: int = Field(..., description="Invoice value Date in epoch milliseconds integer format")
    tags: list[str] = Field(None, description="Invoice tags, array of strings format")
    contactResourceId: str = Field(None, description="The contact resource id, uuidv4 format type")
    internalNotes: str = Field(None, description="Invoice internal notes, string format")
    saveAsDraft: bool = Field(..., description="Save the Invoice as a draft?, this is mandatory and required, default is true, boolean type")
    taxInclusion: bool = Field(None, description="Include Tax for Journal, boolean type")
    taxVatApplicable: bool = Field(None, description="Is Tax Applicable in Journal? boolean type")
    journalEntries: list[CreateJournalEntry] = Field(..., description="Journal Entries json array, this is this is mandatory and minimum 2 entries required, one must be CREDIT and the other DEBIT, format array")
#####################################################
import json
from langchain_core.messages import ToolMessage

class FrekiToolNode:
    """A node that runs the tools requested in the last AIMessage."""

    def __init__(self, api_key: str):
        self.api_key = api_key

    def __call__(self, inputs: dict):
        if messages := inputs.get("messages", []):
            message = messages[-1]
        else:
            raise ValueError("No message found in input")
        outputs = []
        for tool_call in message.tool_calls:
            match tool_call["name"]:
                case "CreateInvoice":
                    tool_call["args"]["valueDate"] = int(tool_call["args"]["valueDate"])
                    output = requestPost(self.api_key, "invoices", tool_call["args"])
                    print(f"CreateInvoice Resp: {output}")
                    outoput = output["data"]
                    output = json.dumps(output)
                    outputs.append(ToolMessage(content=output, tool_call_id=tool_call["id"]))
                case "CreateBill":
                    tool_call["args"]["valueDate"] = int(tool_call["args"]["valueDate"])
                    output = requestPost(self.api_key, "bills", tool_call["args"])
                    print(f"CreateInvoice Resp: {output}")
                    outoput = output["data"]
                    output = json.dumps(output)
                    outputs.append(ToolMessage(content=output, tool_call_id=tool_call["id"]))
                case "CreateJournal":
                    tool_call["args"]["valueDate"] = int(tool_call["args"]["valueDate"])
                    output = requestPost(self.api_key, "journals", tool_call["args"])
                    print(f"CreateInvoice Resp: {output}")
                    outoput = output["data"]
                    output = json.dumps(output)
                    outputs.append(ToolMessage(content=output, tool_call_id=tool_call["id"]))
                case "GetInvoice":
                    output = requestGet(self.api_key, "invoices", tool_call["args"]["resourceId"])
                    #print(f"GetInvoice: {output}")
                    if "data" in output:
                        output = output["data"]
                    output = json.dumps(output)
                    outputs.append(ToolMessage(output, tool_call_id=tool_call["id"]))
                case "GetBill":
                    output = requestGet(self.api_key, "bills", tool_call["args"]["resourceId"])
                    #print(f"GetBill: {output}")
                    if "data" in output:
                        output = output["data"]
                    output = json.dumps(output)
                    outputs.append(ToolMessage(output, tool_call_id=tool_call["id"]))
                case "ListContacts":
                    output = requestList(self.api_key, "contacts")["data"]
                    info = []
                    for contact in output:
                        info.append({"contactResourceId": contact["resourceId"], "name": contact["name"], "email": contact["email"]})
                    output = json.dumps(info)
                    outputs.append(ToolMessage(output, tool_call_id=tool_call["id"]))
                case "ListInvoices":
                    output = requestList(self.api_key, "invoices")["data"]
                    output = json.dumps(output)
                    outputs.append(ToolMessage(output, tool_call_id=tool_call["id"]))
                case "ListBills":
                    output = requestList(self.api_key, "bills")["data"]
                    output = json.dumps(output)
                    outputs.append(ToolMessage(output, tool_call_id=tool_call["id"]))
                case "ListChartOfAccounts":
                    output = requestList(self.api_key, "chart-of-accounts")["data"]
                    output = json.dumps(output)
                    outputs.append(ToolMessage(output, tool_call_id=tool_call["id"]))   
                case "ListTaxProfiles":
                    output = requestList(self.api_key, "vat-profiles")["data"]
                    output = json.dumps(output)
                    outputs.append(ToolMessage(output, tool_call_id=tool_call["id"])) 
                case "ListJournals":
                    output = requestList(self.api_key, "journals")["data"]
                    output = json.dumps(output)
                    outputs.append(ToolMessage(output, tool_call_id=tool_call["id"])) 
        return {"messages": outputs}
#####################################################

from langgraph.prebuilt import ToolNode, tools_condition
from typing import Annotated, Sequence, TypedDict
from langchain_core.messages import BaseMessage
from langgraph.graph import StateGraph
import operator

class State(TypedDict):
    messages: Annotated[Sequence[BaseMessage], operator.add]

tools = [
    CreateInvoice, GetInvoice, ListContacts, ListInvoices,
    ListBills, ListChartOfAccounts, ListTaxProfiles,
    CreateJournal, ListJournals
]
llm_with_tools = llm.bind_tools(tools)

def chatbot(state: State):
    return {"messages": [llm_with_tools.invoke(state["messages"])]}

def start_llm_chat(api_key: str):
    tool_node = FrekiToolNode(api_key)
    graph_builder = StateGraph(State)
    graph_builder.add_node("chatbot", chatbot)
    graph_builder.add_node("tools", tool_node)
    graph_builder.add_conditional_edges("chatbot", tools_condition)
    graph_builder.add_edge("tools", "chatbot")
    graph_builder.set_entry_point("chatbot")
    return graph_builder.compile()