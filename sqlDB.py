from config import sqlConnection

myDB, myCursor = sqlConnection()

# * Added all details in sql.


def ytSqlAddData(jsonResponse):

    # * Added channel details to sql.
    myCursor.execute(f'''
                    INSERT INTO ytChannel (channel_id, custom_url, channel_name, video_count, subscription_count, channel_views, channel_description, channel_thumbnail) 
                    VALUES (
                    "{jsonResponse["Channel_Name"]["Channel_Id"]}",
                    "{jsonResponse["Channel_Name"]["Custom_URL"]}",
                    "{jsonResponse["Channel_Name"]["Channel_Name"]}",
                    "{jsonResponse["Channel_Name"]["Video_Count"]}",
                    "{jsonResponse["Channel_Name"]["Subscription_Count"]}",
                    "{jsonResponse["Channel_Name"]["Channel_Views"]}",
                    "{jsonResponse["Channel_Name"]["Channel_Description"]}",
                    "{jsonResponse["Channel_Name"]["Thumbnail"]}"  
                    )
                    ''')

    for playlistItems in jsonResponse["Channel_Name"]["Playlists"]:

        # * Added playlist details to sql.
        myCursor.execute(f'''
            INSERT INTO ytPlaylist (playlist_id, channel_id, playlist_name)
            VALUES (
                "{jsonResponse["Channel_Name"]["Playlists"][playlistItems]["Playlist_Id"]}",
                "{jsonResponse["Channel_Name"]["Channel_Id"]}",
                "{jsonResponse["Channel_Name"]["Playlists"][playlistItems]["Playlist_Title"]}"
            )
        ''')

        # * Added video details to sql.
        for videoItems in jsonResponse["Channel_Name"]["Playlists"][playlistItems]["Videos"]:
            myCursor.execute(f'''
            INSERT INTO ytVideo (video_id, playlist_id, video_name, video_description, video_publishedAt, video_viewCount, video_likeCount, video_favCount, video_commentCount, video_duration, video_thumbnail)
            VALUES (
                "{jsonResponse["Channel_Name"]["Playlists"][playlistItems]["Videos"][videoItems]["Video_Id"]}",
                "{jsonResponse["Channel_Name"]["Playlists"][playlistItems]["Playlist_Id"]}",
                "{jsonResponse["Channel_Name"]["Playlists"][playlistItems]["Videos"][videoItems]["Video_Name"]}",
                "{jsonResponse["Channel_Name"]["Playlists"][playlistItems]["Videos"][videoItems]["Video_Description"]}",
                "{jsonResponse["Channel_Name"]["Playlists"][playlistItems]["Videos"][videoItems]["PublishedAt"]}",
                "{jsonResponse["Channel_Name"]["Playlists"][playlistItems]["Videos"][videoItems]["View_Count"]}",
                "{jsonResponse["Channel_Name"]["Playlists"][playlistItems]["Videos"][videoItems]["Like_Count"]}",
                "{jsonResponse["Channel_Name"]["Playlists"][playlistItems]["Videos"][videoItems]["Favorite_Count"]}",
                "{jsonResponse["Channel_Name"]["Playlists"][playlistItems]["Videos"][videoItems]["Comment_Count"]}",
                "{jsonResponse["Channel_Name"]["Playlists"][playlistItems]["Videos"][videoItems]["Duration"]}",
                "{jsonResponse["Channel_Name"]["Playlists"][playlistItems]["Videos"][videoItems]["Thumbnail"]}"              
            )
        ''')

            # * Added comment details to sql.
            for commentItem in jsonResponse["Channel_Name"]["Playlists"][playlistItems]["Videos"][videoItems]["Comments"]:
                myCursor.execute(f'''
                INSERT INTO ytComment (comment_id, video_id, comment_text, comment_author, comment_publishedAt)
                VALUES (
                    "{jsonResponse["Channel_Name"]["Playlists"][playlistItems]["Videos"][videoItems]["Comments"][commentItem]["Comment_Id"]}",
                    "{jsonResponse["Channel_Name"]["Playlists"][playlistItems]["Videos"][videoItems]["Video_Id"]}",
                    "{jsonResponse["Channel_Name"]["Playlists"][playlistItems]["Videos"][videoItems]["Comments"][commentItem]["Comment_Text"]}",
                    "{jsonResponse["Channel_Name"]["Playlists"][playlistItems]["Videos"][videoItems]["Comments"][commentItem]["Comment_Author"]}",
                    "{jsonResponse["Channel_Name"]["Playlists"][playlistItems]["Videos"][videoItems]["Comments"][commentItem]["Comment_PublishedAt"]}"
                )
            ''')

    myDB.commit()
    # myCursor.close()
    # myDB.close()


# TODO : sql delete one and delete all.
def ytSqlDelOne(delId):
    myCursor.execute(
        f'''
            SELECT ytCh.channel_id, ytP.playlist_id, ytV.video_id, ytC.comment_id   
            FROM (((ytComment ytC
            INNER JOIN ytVideo ytV ON ytC.video_id = ytV.video_id)
            INNER JOIN ytPlaylist ytP ON ytV.playlist_id = ytP.playlist_id)            
            INNER JOIN ytChannel ytCh ON ytP.channel_id = ytCh.channel_id)
            WHERE ytCh.channel_id = "{delId}"
            ;
                 '''
    )
    # result = myCursor.fetchall()
    comment_id = [row[3] for row in myCursor]
    comment_id = list(set(comment_id))

    for comment_ids in comment_id:
        myCursor.execute(
            f"DELETE FROM ytComment WHERE comment_id = '{comment_ids}';")
        myCursor.execute(
            f"DELETE FROM ytVideo WHERE video_id IN (SELECT video_id FROM ytComment WHERE comment_id = '{comment_ids}');")
        myCursor.execute(
            f"DELETE FROM ytPlaylist WHERE playlist_id IN (SELECT playlist_id FROM ytVideo WHERE video_id IN (SELECT video_id FROM ytComment WHERE comment_id = '{comment_ids}'));")
        myCursor.execute(
            f"DELETE FROM ytChannel WHERE channel_id IN (SELECT channel_id FROM ytPlaylist WHERE playlist_id IN (SELECT playlist_id FROM ytVideo WHERE video_id IN (SELECT video_id FROM ytComment WHERE comment_id = '{comment_ids}')));")

    myDB.commit()
    # myCursor.close()
    # myDB.close()


def ytSqlDelAll():
    myCursor.execute("DELETE FROM ytComment;")
    myCursor.execute("DELETE FROM ytVideo;")
    myCursor.execute("DELETE FROM ytPlaylist;")
    myCursor.execute("DELETE FROM ytChannel;")

    myDB.commit()
    # myCursor.close()
    # myDB.close()
