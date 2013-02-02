import os
import json
import codecs

def json_path(filename):
    return os.path.join(os.path.abspath(os.path.dirname(__name__)), filename)

def load_video_json(filename):
    with codecs.open(json_path(filename), encoding='utf-8') as fp:
        return json.load(fp)

if __name__ == '__main__':
    print load_video_json("videos.json")
    print load_video_json("test-videos.json")
