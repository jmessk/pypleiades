from pymec_client.mec_developer import MECDeveloper, AsyncMECDeveloper


# Sync version
def main():
    server_url = "https://mecrm.dolylab.cc/api/v0.5"

    developer = MECDeveloper(server_url)

    # Create a lambda bytes
    lambda_bytes = b"""\
const message: string = "Hello, TypeScript!";
console.log(message);
"""

    # Get the lambda id
    lambda_id = developer.create_lambda_by_bytes(lambda_bytes, "typescript+helloworld")

    # You can also create a lambda by posting the lambda data

    # lambda_data_id = developer.post_data(lambda_bytes)
    # lambda_id = developer.create_lambda_by_id(lambda_data_id, "pymec+echo")

    print(lambda_id)


# Async version
async def async_main():
    server_url = "https://mecrm.dolylab.cc/api/v0.5"

    developer = AsyncMECDeveloper(server_url)

    # Create a lambda bytes
    lambda_bytes = b"""\
const message: string = "Hello, TypeScript!";
console.log(message);
"""

    # Get the lambda id
    lambda_id = await developer.create_lambda_by_bytes(lambda_bytes, "typescript+helloworld")

    # You can also create a lambda by posting the lambda data

    # lambda_data_id = await developer.post_data(lambda_bytes)
    # lambda_id = await developer.create_lambda_by_id(lambda_data_id, "pymec+echo")

    print(lambda_id)


if __name__ == "__main__":
    main()
