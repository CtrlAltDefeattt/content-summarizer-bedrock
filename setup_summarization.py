import boto3
from botocore.exceptions import ClientError
from summarization_lib import BEDROCK_REGION, DEFAULT_MODEL_ID


def main():
    print("Checking AWS Bedrock configuration...\n")
    print(f"Region: {BEDROCK_REGION}")
    print(f"Model ID: {DEFAULT_MODEL_ID}\n")

    try:
        client = boto3.client("bedrock-runtime", region_name=BEDROCK_REGION)

        # Quick health check: try a tiny call
        response = client.converse(
            modelId=DEFAULT_MODEL_ID,
            messages=[{
                "role": "user",
                "content": [{"text": "Say 'OK' if you can read this."}]
            }],
            inferenceConfig={"maxTokens": 10, "temperature": 0.0}
        )

        output = response["output"]["message"]["content"][0]["text"]
        print("Bedrock call successful!")
        print("Model replied:", output)

    except ClientError as e:
        print("❌ AWS ClientError when calling Bedrock.")
        print("Details:", e)
    except Exception as e:
        print("❌ Unexpected error.")
        print("Details:", e)


if __name__ == "__main__":
    main()
