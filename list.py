import dropbox
import os
import argparse
from urllib.parse import urlparse, parse_qs, urlunparse

DROPBOX_ACCESS_TOKEN = os.environ.get("DROPBOX_ACCESS_TOKEN")


def get_dropbox_links(token, sort_by):
    dbx = dropbox.Dropbox(token)
    try:
        files = dbx.files_list_folder("")
        links = []
        for entry in files.entries:
            if isinstance(entry, dropbox.files.FileMetadata):
                try:
                    shared_link_metadata = dbx.sharing_create_shared_link_with_settings(
                        entry.path_lower
                    )
                    link = shared_link_metadata.url
                except dropbox.exceptions.ApiError as err:
                    if err.error.is_shared_link_already_exists():
                        shared_links = dbx.sharing_list_shared_links(
                            path=entry.path_lower
                        ).links
                        if shared_links:
                            link = shared_links[0].url
                    else:
                        print(f"共有リンクの取得に失敗しました。エラー: {err}")
                        continue
                # リンクとメタデータを保存
                links.append((entry, link))

        # ソート基準に応じてソート
        if sort_by == "name":
            sorted_links = sorted(links, key=lambda x: x[0].name.lower())
        elif sort_by == "date":
            sorted_links = sorted(
                links, key=lambda x: x[0].client_modified, reverse=True
            )
        else:
            raise ValueError("Unsupported sort option. Choose 'name' or 'date'.")

        # ソートされたリンクを表示
        for entry, link in sorted_links:
            print(
                f"ファイル名: {entry.name}, アップロード日時: {entry.client_modified}, リンク: {link}"
            )

    except dropbox.exceptions.ApiError as err:
        print(f"フォルダ一覧の取得に失敗しました。エラー: {err}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Dropbox files shared links retriever."
    )
    parser.add_argument(
        "--sort-by",
        type=str,
        choices=["name", "date"],
        default="name",
        help="Sort files by name or upload date.",
    )
    args = parser.parse_args()

    get_dropbox_links(DROPBOX_ACCESS_TOKEN, args.sort_by)
