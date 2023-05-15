# Opinion AI API Documentation
This documentation provides an overview of the endpoints and functionality of the Flask API.


## Base URL
The base URL for all API endpoints is: `http://localhost:5000`

## Endpoints
### 1. Aspects Endpoints
#### Create a new Aspect
- Endpoint: `/api/aspects`
- Method: `POST`
- Description: Create a new Aspect
- Request Body:
  ```json
  {
    "aspect": "room",
  }
- Response:
  ```json
  {
    "aspect": "room",
    "pid": "e4124ba4-9a3e-4ef9-ae49-2eb15b953bc3"
  }
#### Get All Aspects
- Endpoint: `/api/aspects`
- Method: `GET`
- Description: Get a list of all aspects
- Response:
  ```json
  [
    {
      "aspect": "room",
      "pid": "e4124ba4-9a3e-4ef9-ae49-2eb15b953bc3"
    },
    {
      "aspect": "stuff",
      "pid": "2de2bff2-e7be-4e03-ba21-9907e42a669a"
    }
  ]
### 2. Sentiments Endpoints
#### Create a new Sentiment
- Endpoint: `/api/sentiments`
- Method: `POST`
- Description: Create a new sentiment
- Request Body:
  ```json
  {
    "sentiments": "POS"
  }
- Response:
  ```json
  {
    "pid": "bb1446fa-752b-4950-91f9-2f038aad8c1d",
    "sentiment": "POS"
  }
#### Get All Sentiments
- Endpoint: `/api/sentiments`
- Method: `GET`
- Description: Get a list of all sentiments
- Response:
  ```json
  [
    {
      "pid": "bb1446fa-752b-4950-91f9-2f038aad8c1d",
      "sentiment": "POS"
    },
    {
      "pid": "4ff973fc-41c3-4609-966d-59a82178f33a",
      "sentiment": "NEG"
    },
    {
      "pid": "3ecda40b-04fa-4ff5-8ef4-1322da7e903e",
      "sentiment": "NEU"
    }
  ]
### 3. Tags Endpoints
#### Insert a Tag
- Endpoint: `/api/tags`
- Method: `POST`
- Description: Insert a Tag
- Request Body:
  ```json
  {
    "aspect": "e4124ba4-9a3e-4ef9-ae49-2eb15b953bc3"
    "sentiment": "bb1446fa-752b-4950-91f9-2f038aad8c1d"
  }
- Response:
  ```json
  {
    "aspect": {
      "aspect": "room",
      "pid": "e4124ba4-9a3e-4ef9-ae49-2eb15b953bc3"
    },
    "pid": "cabd80a5-479d-4f9f-bf1f-71994a412633",
    "sentiment": {
      "pid": "bb1446fa-752b-4950-91f9-2f038aad8c1d",
      "sentiment": "POS"
    }
  }
#### Get All Tags
- Endpoint: `/api/tags`
- Method: `GET`
- Description: Get a list of all tags
- Response:
  ```json
  [
    {
      "aspect": {
        "aspect": "room",
        "pid": "e4124ba4-9a3e-4ef9-ae49-2eb15b953bc3"
      },
      "pid": "cabd80a5-479d-4f9f-bf1f-71994a412633",
      "sentiment": {
        "pid": "bb1446fa-752b-4950-91f9-2f038aad8c1d",
        "sentiment": "POS"
      }
    },
    {
      "aspect": {
        "aspect": "stuff",
        "pid": "2de2bff2-e7be-4e03-ba21-9907e42a669a"
      },
      "pid": "a88ee312-5037-4d65-a2af-b8b9b5489dba",
      "sentiment": {
        "pid": "4ff973fc-41c3-4609-966d-59a82178f33a",
        "sentiment": "NEG"
      }
    }
  ]
### 4. Hltddbs Endpoints
#### Create a new Hltddbs (Human Level Text & Document Database)
- Endpoint: `/api/hltddbs`
- Method: `POST`
- Description: Get a list of all aspects
- Request Body:
  ```json
  {
    "text": "The Room was terrible but the staff was very friendly.",
  }
- Response:
  ```json
  {
    "pid": "8af02b90-9e4c-4098-b19b-411b06f34a08",
    "tags": [],
    "text": "The Room was terrible but the staff was very friendly."
  }
#### Labeling
- Endpoint: `/hltddb/<string:hltddb_pid>/<string:aspect_pid>`
- Method: `POST`
- Description: Set sentiment of hltddbs-aspect
- Request URL: `http://localhost:5000/api/hltddbs/hltddb/8af02b90-9e4c-4098-b19b-411b06f34a08/e4124ba4-9a3e-4ef9-ae49-2eb15b953bc3`
- Request Body:
  ```json
  {
    "sentiment": "4ff973fc-41c3-4609-966d-59a82178f33a"
  }
- Response:
  ```json
  {
    "hltddb_pid": "8af02b90-9e4c-4098-b19b-411b06f34a08"
  }
#### Get All Hltddbs
- Endpoint: `/api/hltddbs`
- Method: `GET`
- Description: Get a list of all hltddbs
- Response:
  ```json
  [
    {
      "pid": "8af02b90-9e4c-4098-b19b-411b06f34a08",
      "tags": [
        {
          "aspect": "room",
          "pid": "0cedf915-6e94-45cf-8bcc-7bc99fe9549e",
          "sentiment": "NEG"
        }
      ],
      "text": "The Room was terrible but the staff was very friendly."
    }
  ]
#### Upload Hltddbs File in csv format
- Endpoint: `/api/hltddbs/file`
- Method: `POST`
- Description: Upload hltddbs file in csv format
- Request Body:
  - CSV File

    | Text                                                                       |
    |----------------------------------------------------------------------------|
    | The Room was terrible but the staff was very friendly.                     |
    | The concert was electrifying, and the crowd was filled with energy.        |
    | The movie was captivating, with an unexpected twist at the end.            |
    | The cake was delicious, with layers of rich chocolate and creamy frosting. |
    | The hike was challenging, but the breathtaking views made it worth it.     |
  - Format
    ```json
    "csv_file": data.csv
- Response:
  ```json
  {
    "total": 5
  }
#### Upload Hltddbs File in csv format
- Endpoint: `/api/hltddbs/file`
- Method: `GET`
- Description: Download hltddbs file in csv format
- Response

  | pid                                  | text                                                                         | tags                                                                                                  |
  |--------------------------------------|------------------------------------------------------------------------------|-------------------------------------------------------------------------------------------------------|
  | 8af02b90-9e4c-4098-b19b-411b06f34a08 | The Room was terrible but the staff was very friendly.                       | "[{""pid"": ""0cedf915-6e94-45cf-8bcc-7bc99fe9549e"", ""aspect"": ""room"", ""sentiment"": ""NEG""}]" |
  | aaa410f5-55da-4b5b-80ab-ab2c788e966d | The Room was terrible but the staff was very friendly.                       | []                                                                                                    |
  | 96d4f9cb-c1dd-4fa2-86b1-4b497e7d566d | "The concert was electrifying, and the crowd was filled with energy."        | []                                                                                                    |
  | b53484b2-cf13-475b-8ebf-82ca31e361af | "The movie was captivating, with an unexpected twist at the end."            | []                                                                                                    |
  | 1f73df83-c669-4109-80ad-e590c921ee82 | "The cake was delicious, with layers of rich chocolate and creamy frosting." | []                                                                                                    |