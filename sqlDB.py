from config import sqlConnection

myDB, myCursor = sqlConnection()

# * Added all details in sql.


def ytSqlAddData(jsonResponse):

    # * Added channel details to sql.

    channelSql = '''
    INSERT INTO ytChannel (channel_id, custom_url, channel_name, video_count, subscription_count, channel_views, channel_description, channel_thumbnail) 
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    '''
    channelValues = (
        jsonResponse["Channel_Name"]["Channel_Id"],
        jsonResponse["Channel_Name"]["Custom_URL"],
        jsonResponse["Channel_Name"]["Channel_Name"],
        jsonResponse["Channel_Name"]["Video_Count"],
        jsonResponse["Channel_Name"]["Subscription_Count"],
        jsonResponse["Channel_Name"]["Channel_Views"],
        jsonResponse["Channel_Name"]["Channel_Description"],
        jsonResponse["Channel_Name"]["Thumbnail"]
    )

    myCursor.execute(channelSql, channelValues)

    playlistSql = '''
                INSERT INTO ytPlaylist (playlist_id, channel_id, playlist_name) 
                VALUES (%s, %s, %s)
                '''

    for playlistItems in jsonResponse["Channel_Name"]["Playlists"]:

        # * Added playlist details to sql.
        palylistValues = (
            jsonResponse["Channel_Name"]["Playlists"][playlistItems]["Playlist_Id"],
            jsonResponse["Channel_Name"]["Channel_Id"],
            jsonResponse["Channel_Name"]["Playlists"][playlistItems]["Playlist_Title"]
        )

        myCursor.execute(playlistSql, palylistValues)

        videoSql = '''
                        INSERT INTO ytVideo (video_id, playlist_id, video_name, video_description, video_publishedAt, video_viewCount, video_likeCount, video_favCount, video_commentCount, video_duration, video_thumbnail) 
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                        '''

        # * Added video details to sql.
        for videoItems in jsonResponse["Channel_Name"]["Playlists"][playlistItems]["Videos"]:
            videoValues = (
                jsonResponse["Channel_Name"]["Playlists"][playlistItems]["Videos"][videoItems]["Video_Id"],
                jsonResponse["Channel_Name"]["Playlists"][playlistItems]["Playlist_Id"],
                jsonResponse["Channel_Name"]["Playlists"][playlistItems]["Videos"][videoItems]["Video_Name"],
                jsonResponse["Channel_Name"]["Playlists"][playlistItems]["Videos"][videoItems]["Video_Description"],
                jsonResponse["Channel_Name"]["Playlists"][playlistItems]["Videos"][videoItems]["PublishedAt"],
                jsonResponse["Channel_Name"]["Playlists"][playlistItems]["Videos"][videoItems]["View_Count"],
                jsonResponse["Channel_Name"]["Playlists"][playlistItems]["Videos"][videoItems]["Like_Count"],
                jsonResponse["Channel_Name"]["Playlists"][playlistItems]["Videos"][videoItems]["Favorite_Count"],
                jsonResponse["Channel_Name"]["Playlists"][playlistItems]["Videos"][videoItems]["Comment_Count"],
                jsonResponse["Channel_Name"]["Playlists"][playlistItems]["Videos"][videoItems]["Duration"],
                jsonResponse["Channel_Name"]["Playlists"][playlistItems]["Videos"][videoItems]["Thumbnail"]
            )

            myCursor.execute(videoSql, videoValues)

            commentSql = '''
                                INSERT INTO ytComment (comment_id, video_id, comment_text, comment_author, comment_publishedAt) 
                                VALUES (%s, %s, %s, %s, %s)
                                '''

            # * Added comment details to sql.
            for commentItem in jsonResponse["Channel_Name"]["Playlists"][playlistItems]["Videos"][videoItems]["Comments"]:

                commentValues = (
                    jsonResponse["Channel_Name"]["Playlists"][playlistItems]["Videos"][videoItems]["Comments"][commentItem]["Comment_Id"],
                    jsonResponse["Channel_Name"]["Playlists"][playlistItems]["Videos"][videoItems]["Video_Id"],
                    jsonResponse["Channel_Name"]["Playlists"][playlistItems]["Videos"][videoItems]["Comments"][commentItem]["Comment_Text"],
                    jsonResponse["Channel_Name"]["Playlists"][playlistItems]["Videos"][videoItems]["Comments"][commentItem]["Comment_Author"],
                    jsonResponse["Channel_Name"]["Playlists"][playlistItems]["Videos"][
                        videoItems]["Comments"][commentItem]["Comment_PublishedAt"]
                )

                myCursor.execute(commentSql, commentValues)

    myDB.commit()
    # myCursor.close()
    # myDB.close()


def ytSqlDelOne(delId):

    query = "DELETE FROM ytChannel WHERE channel_id = %s"
    myCursor.execute(query, (delId,))   
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

