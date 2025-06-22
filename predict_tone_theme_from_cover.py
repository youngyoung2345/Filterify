import os
import base64
import argparse
import pandas as pd
import openai

def read_text(text_path):
    with open(text_path, 'r', encoding='utf-8') as f:
        return f.read().strip()

def import_csv_as_pd(csv_path):
    return pd.read_csv(csv_path, encoding='cp949') 

def encode_image(image_path):
    with open(image_path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")

def get_features(prompt, encoded_image):
    try:
        response = openai.chat.completions.create(
            model="gpt-4-turbo",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt},
                        {"type": "image_url", "image_url": {
                            "url": f"data:image/jpeg;base64,{encoded_image}"
                        }}
                    ]
                }
            ],
            max_tokens=300
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"ERROR: {e}"

def modify_df(images_path, prompt, df):
    df['tone'], df['theme'] = "", ""
    feature_cache = {}

    for index, row in df.iterrows():
        try:
            image_name = row['image_path']
            full_image_path = os.path.join(images_path, image_name)

            if image_name in feature_cache:
                tone, theme = feature_cache[image_name]
            else:
                encoded = encode_image(full_image_path)
                response = get_features(prompt, encoded)

                if "The tone" in response and "The theme" in response:
                    parts = response.split("The theme")
                    tone = parts[0].strip()
                    theme = "The theme " + parts[1].strip()
                else:
                    tone = response
                    theme = ""

                feature_cache[image_name] = (tone, theme)

            df.at[index, 'tone'] = tone
            df.at[index, 'theme'] = theme

        except Exception as e:
            print(f"Error at row {index}, image: {image_name}, error: {e}")
            continue

    return df

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--key_path', type=str)
    parser.add_argument('--prompt_path', type=str)
    parser.add_argument('--csv_path', type=str)
    parser.add_argument('--images_path', type=str)
    parser.add_argument('--out_path', type=str)
    args = parser.parse_args()

    openai.api_key = read_text(args.key_path)
    prompt = read_text(args.prompt_path)

    df = import_csv_as_pd(args.csv_path)
    df = modify_df(args.images_path, prompt, df)

    df.to_csv(args.out_path, index=False, encoding='utf-8')

if __name__ == "__main__":
    main()
