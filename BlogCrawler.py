"""
블로그 데이터 스크래핑.
"""
from naver import NaverBlogCrawler, NaverPostCrawler
from tistory import TistoryBlogCrawler, TistoryPostCrawler
from enum import Enum
import time
import random


class SupportPlatform(Enum):
    """
    지원되는 플랫폼에 대한 enum 리스트
    """
    Naver = 0
    Tistory = 1

    def __str__(self):
        return self.name


def read(platform, blog_id, category_id, include_child=False):
    platform = convert_platform_id(platform)
    if not platform:
        # 지원되지 않는 플랫폼인 경우
        raise

    df = read_list_in_category(platform, blog_id, category_id, include_child)
    df.insert(3, 'contents', '')

    total_count = len(df)
    for idx, row in df.iterrows():
        post_id = row['post_id']
        count = df.index.get_loc(idx) + 1
        # count = int(idx)+1
        print(f"read_post ({platform}, {blog_id}, {post_id})  {count}/{total_count}")
        row['contents'] = read_post(platform, blog_id, post_id)

        # 혹시 모르니까 sleep 추가
        time.sleep(get_sleep_time_random())
    return df


def get_sleep_time_random():
    rv = random.random() * 10 + 2
    return rv


def to_text(df, file_name, reverse=False):
    if reverse:
        df = df[::-1]

    # 파일에 쓰기
    with open(file_name, 'wt', encoding='utf-8') as f:
        for idx, row in df.iterrows():
            # f.write('================================')
            f.write("\n")
            f.write(f"제목 : {row['title']}\n")
            f.write(f"작성일 : {row['created_at'].date()}\n\n")
            f.write(row['contents'])
            f.write("\n\n\n\n")
    return True


def read_list_in_category(blog_platform, blog_id, category_id, include_child=False):
    platform = convert_platform_id(blog_platform)
    if platform == SupportPlatform.Naver:
        return NaverBlogCrawler.read_list_in_category(blog_id, category_id, include_child)
    elif platform == SupportPlatform.Tistory:
        return TistoryBlogCrawler.read_list_in_category(blog_id, category_id, include_child)
    else:
        return False


def read_post(blog_platform, blog_id, post_id):
    # print(f"read_post ({blog_platform}, {blog_id}, {post_id})")
    platform = convert_platform_id(blog_platform)
    if platform == SupportPlatform.Naver:
        return NaverPostCrawler.read_post(blog_id, post_id)
    elif platform == SupportPlatform.Tistory:
        return TistoryPostCrawler.read_post(blog_id, post_id)
    else:
        return False


def convert_platform_id(platform):
    """
    지원되는 플랫폼에 대한 형식(Enum)으로 전환 및 체크
    :param platform: str|int
    :return: SupportPlatform value
    """
    if isinstance(platform, SupportPlatform):
        return platform

    if isinstance(platform, str):
        p = platform.lower()
        if p == 'naver':
            return SupportPlatform.Naver
        elif p == 'tistory':
            return SupportPlatform.Tistory
        else:
            print('지원되지 않는 블로그 플랫폼입니다.')
            raise
    else:
        raise
