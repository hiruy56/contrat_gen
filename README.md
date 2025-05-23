My first paid project.


chatgpt made docs i was tired ok and i am not about to stye allat
To document the provided FastAPI application that fills in a contract template, you can follow these steps:

### Requirements

Make sure you have the following libraries installed:
- `fastapi`
- `python-docx`

You can install them using pip:
```bash
pip install fastapi python-docx
```

### Code Explanation

Here's a breakdown of the code:

1. **Imports**: Import necessary libraries and modules.

2. **FastAPI Setup**: Initialize a FastAPI instance (`app`).

3. **CORS Middleware**: Allow CORS for POST requests to enable cross-origin requests.

4. **fill_contract_template Function**: This function takes `contract_details` as input, replaces placeholders in a Word document template (`tomp.docx`) with corresponding values from `contract_details`, and returns a `BytesIO` stream of the filled document.

5. **POST Endpoint `/fill-contract`**: Defines a POST endpoint `/fill-contract` that accepts a JSON body (`contract_details`) containing the data to fill into the contract template. It calls `fill_contract_template` to get the filled document as a stream and returns it as a `StreamingResponse` with media type `application/vnd.openxmlformats-officedocument.wordprocessingml.document`.

6. **Main Execution**: Runs the FastAPI application using Uvicorn server.

### Example Usage

To use this API:

- Ensure `tomp.docx` exists in the same directory as your script, containing placeholders like `{key}` that match the keys in `contract_details`.
- Send a POST request to `http://127.0.0.1:8000/fill-contract` with JSON payload containing your contract details.

### Example python code

```
import requests

# Endpoint URL
url = 'http://127.0.0.1:8000/fill-contract'

# Example contract details
contract_details = {
    'client_name': 'John Doe',
    'company_name': 'ABC Inc.',
    'start_date': '2024-07-05',
    'end_date': '2024-12-31',
    'amount': 5000.00,
}

# Send POST request with JSON payload
response = requests.post(url, json=contract_details)

# Check response status
if response.status_code == 200:
    # Save the filled contract to a file
    with open('filled_contract.docx', 'wb') as f:
        f.write(response.content)
    print("Filled contract saved successfully.")
else:
    print(f"Failed to fill contract. Status code: {response.status_code}")
```

### How to make tomp (example)
`
this was sined on {start_date} and end at {end_date}
client_name: {client_name}
company_name: {company_name}
amount: {amount}
`

the code ubove works for the tomp example the code changes the stuff on the {}  

