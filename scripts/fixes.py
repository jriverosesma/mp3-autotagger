import os


def fix_pafy():
    project_dir = os.path.dirname(os.path.dirname((__file__)))
    with open(project_dir + '\\.venv\\Lib\\site-packages\\pafy\\backend_youtube_dl.py', 'r+') as f:
        lines = f.readlines()
        f.seek(0)
        lines[52] = '#' + lines[52] # Comment 'likes' field
        lines[53] = '#' + lines[53] # Comment 'dislikes' field
        f.writelines(lines)


if __name__ == '__main__':
    fix_pafy()
