import json
import pandas as pd

import argparse

def import_json(json_path): 
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data

def convert_dic_to_list(data):
    header_list = ['album_name', 'artists', 'track_name', 
                   'danceability', 'energy', 'key', 'loudness', 'speechness', 'acousticness', 'instrumentalness', 'liveness', 'valence', 'tempo',
                   'image_path']
    df = pd.DataFrame(columns=header_list)
    
    for key in data.keys():
        content_list = [None] * len(header_list)

        track = data[key]

        album_file = track['image_filename']
        content_list[-1] = album_file

        album_feature = track['original_data']
        for feature_key in album_feature.keys():
            if feature_key in header_list: # if feature_key in ['album_name', 'artists', 'track_name']
                idx = header_list.index(feature_key)
                content_list[idx] = album_feature[feature_key]
            else:
                if feature_key == 'raw_audio_features':
                    audio_feature = album_feature[feature_key]
                    try:
                        for audio_feature_key in audio_feature.keys():
                            idx = header_list.index(audio_feature_key)
                            content_list[idx] = audio_feature[audio_feature_key]
                    except:
                        pass

        df.loc[len(df)] = content_list
    
    return df

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--json_path', type=str)
    parser.add_argument('--out_path', type=str)
    args = parser.parse_args()

    data = import_json(args.json_path)
    df = convert_dic_to_list(data)
    df.to_csv(args.out_path, index=False, encoding='utf-8')

    return

if __name__ == "__main__":
    main()