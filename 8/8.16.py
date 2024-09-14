import pandas as pd
import requests
import json
import os

# Function to send a message and process the response
def send_message(index, row, df):
    message = row['question']
    url = 'http://36.212.171.121:8997/instruct_chat'
    headers = {
        'Content-Type': 'application/json'
    }
    data = {
        'messages': [
            {
                'role': 'user',
                'content': message
            }
        ]
    }
    response = requests.post(url, headers=headers, data=json.dumps(data))
    print(f"请求数据: {message}, response: {response.text}")
    try:
        json_str = response.text.replace('data: ', '', 1)
        data = json.loads(json_str)
        type_value = data.get('type')
        content_value = data.get('content')

        # Update the DataFrame directly with the correct dtype
        df.at[index, 'type'] = str(type_value)  # Ensure type_value is cast to string
        df.at[index, 'content'] = json.dumps(content_value, ensure_ascii=False)  # Ensure content_value is cast to string

    except json.JSONDecodeError as e:
        print("Failed to decode JSON response")
        df.at[index, 'type'] = 'Error'
        df.at[index, 'content'] = 'Error'

# Function to read and send questions from an Excel file and save results to a new file
def read_and_send_xlsx(input_file_path, output_file_path):
    df = pd.read_excel(input_file_path)

    # Ensure 'type' and 'content' columns are of type object (to store strings)
    df['type'] = df['type'].astype('object')
    df['content'] = df['content'].astype('object')

    # Loop through each row and process it one by one
    for index, row in df.iterrows():
        send_message(index, row, df)

    # Save the updated DataFrame to the new Excel file
    with pd.ExcelWriter(output_file_path, engine='openpyxl', mode='w') as writer:
        df.to_excel(writer, index=False)

if __name__ == '__main__':
    # Define the input and output file paths
    input_file_path = '../doc/会议语料1.xlsx'
    output_file_path = '../doc/8.16_processed.xlsx'

    # Ensure the output file doesn't overwrite an existing file
    # if os.path.exists(output_file_path):
    #     os.remove(output_file_path)

    # Call the function with the input file and the path to the new output file
    read_and_send_xlsx(input_file_path, output_file_path)
