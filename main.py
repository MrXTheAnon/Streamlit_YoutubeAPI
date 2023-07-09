import streamlit as st

from youtubeAPI import fetchYtDetails
from config import urlNotValidMsg, urlPresentMsg
from mongoDB import mongoDelOne, mongoDelAll
from sqlDB import ytSqlDelOne, ytSqlDelAll

st.cache_resource.clear()


def main():
    # Connection with sql using streamlit.
    stConn = st.experimental_connection('mysql', type='sql')
    stDF = stConn.query('SELECT * FROM ytChannel;', ttl=60)

    # Custom URL form.
    ytImg, ytTxtImg = st.columns([1, 6])

    # Insert your own custom image or preferred image.
    ytImg.image(image='assets/images/youtube.svg')
    ytTxtImg.image(image='assets/images/youtubeText.svg')

    # Validating and parsing custom url.
    customUrlList = list(stDF.iloc[:]['custom_url'])
    with st.form('customUrlKey', clear_on_submit=True):
        stlitCustURL = st.text_input(
            label='Custom URL', placeholder='eg: @rohith97sri02')
        submit_button = st.form_submit_button(
            label='Submit', use_container_width=True)

    if submit_button:
        if stlitCustURL == '' or not stlitCustURL.startswith('@'):
            st.error(urlNotValidMsg, icon='🔗')
        elif stlitCustURL in customUrlList:
            st.error(urlPresentMsg, icon='📺')
        else:
            fetchYtDetails(stlitCustURL)

    # Channel list form.
    channelList = list(stDF.iloc[:]['channel_name'])
    with st.form('listForm', clear_on_submit=True):
        stlitListAllChannel = st.selectbox(
            "Channel List", channelList)

        selButton, delButton, clearButton = st.columns(3)

    # Retreiving or deleting values from sql.
    if selButton.form_submit_button(label='Select', use_container_width=True):
        # Channel details list.
        listDestails = list(
            stDF.loc[stDF['channel_name'] == stlitListAllChannel].iloc[:, 2:8].values)

        # Column : Details for selected channel.
        ytImg, ytTxt, ytSubCount, ytVideoCount, ytChView = st.columns([
            1, 2, 2, 2, 2])
        ytImg.image(listDestails[0][5], width=60)
        ytTxt.markdown(
            f"<h4 style='text-align: justify; color: #FAFAFA;'>{listDestails[0][0]}</h4>", unsafe_allow_html=True)
        # ytCounts.dataframe(stDF.loc[stDF['channel_name']==stlitListAllChannel].iloc[:,3:5], hide_index=True)
        ytSubCount.markdown(
            "<h5 style='text-align: center; color: #FAFAFA;'>Sub Count</h5>", unsafe_allow_html=True)
        ytSubCount.markdown(
            f"<h5 style='text-align: center; color: #FAFAFA;'>{int(listDestails[0][2]):,}</h5>", unsafe_allow_html=True)
        ytVideoCount.markdown(
            "<h5 style='text-align: center; color: #FAFAFA;'>Video Count</h5>", unsafe_allow_html=True)
        ytVideoCount.markdown(
            f"<h5 style='text-align: center; color: #FAFAFA;'>{int(listDestails[0][1]):,}</h5>", unsafe_allow_html=True)
        ytChView.markdown(
            "<h5 style='text-align: center; color: #FAFAFA;'>Channel Views</h5>", unsafe_allow_html=True)
        ytChView.markdown(
            f"<h5 style='text-align: center; color: #FAFAFA;'>{int(listDestails[0][3]):,}</h5>", unsafe_allow_html=True)

    # * Deletes all from mongo and sql.
    if clearButton.form_submit_button(label='Clear', use_container_width=True):
        mongoDelAll()
        ytSqlDelAll()

    # * Delete selected from mongo and sql.
    if delButton.form_submit_button(label='Delete', use_container_width=True):
        # Retreiving channel_id to pass through mongo and sql deletion.
        selectedChannelName = stDF.loc[stDF['channel_name']
                                       == stlitListAllChannel].iloc[0, 0]
        mongoDelOne(delId=selectedChannelName)
        ytSqlDelOne(delId=str(selectedChannelName))

    listAll = st.container()
    with listAll:
        # Channels present in sql with channel thumbnails.
        if len(stDF['channel_thumbnail']) == 0:
            st.image(
                "https://yt3.googleusercontent.com/ytc/AGIKgqNenz9U6NV-2OP1j0DVVzg1i6gqHYiZ3ohYZ1lIKw=s900-c-k-c0x00ffffff-no-rj", width=50)
            st.write('Try adding channel name eg. @rohith97sri02')
        else:
            imgColumn = st.columns(len(stDF['channel_thumbnail']))
            for index, channelThumb in enumerate(stDF['channel_thumbnail'].values):
                imgColumn[index].image(channelThumb, width=60)

        st.subheader('Channel List')
        st.dataframe(stDF.iloc[:, 2:6].head(
            10), hide_index=True, use_container_width=True)

        # SQL Queries
        # Q1
        stDFQ1 = stConn.query(
            '''
                SELECT ytCh.channel_name AS "Channel Name", ytV.video_name AS "Video Name"
                FROM ((ytVideo ytV
                INNER JOIN ytPlaylist ytP ON ytV.playlist_id = ytP.playlist_id)
                INNER JOIN ytChannel ytCh ON ytP.channel_id = ytCh.channel_id);
                    ''',
            ttl=60
        )
        st.subheader('Channel and Video Names')
        st.dataframe(stDFQ1.sort_values('Channel Name').head(
            10), hide_index=True, use_container_width=True)

        # Q2
        st.subheader('High videos channel')
        st.dataframe(stConn.query(
            'SELECT channel_name AS "Channel Name", video_count AS "Video Count" FROM ytChannel ORDER BY video_count DESC;').head(10), hide_index=True, use_container_width=True)
        # st.dataframe(stDF.iloc[:, 2:4].sort_values(
        #       'video_count', ascending=False).head(10), hide_index=True, use_container_width=True)

        # Q3
        stDFQ1 = stConn.query(
            '''
                SELECT ytCh.channel_name AS "Channel Name", ytV.video_name AS "Video Name", ytV.video_viewCount AS "Video Views"
                FROM ((ytVideo ytV
                INNER JOIN ytPlaylist ytP ON ytV.playlist_id = ytP.playlist_id)
                INNER JOIN ytChannel ytCh ON ytP.channel_id = ytCh.channel_id);
                    ''',
            ttl=60
        )
        st.subheader('High video views')
        st.dataframe(stDFQ1.sort_values(
            'Video Views', ascending=False).head(10), hide_index=True, use_container_width=True)

        # Q4 & Q10
        stDFQ1 = stConn.query(
            '''
                SELECT ytV.video_name AS "Video Name", ytV.video_commentCount AS "Comment Count", ytCh.channel_name AS "Channel Name"
                FROM ((ytVideo ytV
                INNER JOIN ytPlaylist ytP ON ytV.playlist_id = ytP.playlist_id)
                INNER JOIN ytChannel ytCh ON ytP.channel_id = ytCh.channel_id);
                    ''',
            ttl=60
        )
        st.subheader('High comment by channel name and video name')
        st.dataframe(stDFQ1.sort_values(
            'Comment Count', ascending=False).head(10), hide_index=True, use_container_width=True)

        # Q5
        stDFQ1 = stConn.query(
            '''
                SELECT ytCh.channel_name AS "Channel Name", ytV.video_likeCount AS "Like Count"
                FROM ((ytVideo ytV
                INNER JOIN ytPlaylist ytP ON ytV.playlist_id = ytP.playlist_id)
                INNER JOIN ytChannel ytCh ON ytP.channel_id = ytCh.channel_id);
                    ''',
            ttl=60
        )
        st.subheader('High video like by video name')
        st.dataframe(stDFQ1.sort_values(
            'Like Count', ascending=False).head(10), hide_index=True, use_container_width=True)

        # Q6 Youtube removed dislike.
        stDFQ1 = stConn.query(
            '''
                SELECT ytV.video_name AS "Video Name", ytV.video_likeCount AS "Video Like Count"
                FROM ytVideo ytV
                    ''',
            ttl=60
        )
        st.subheader('High video like')
        st.dataframe(stDFQ1.sort_values(
            'Video Like Count', ascending=False).head(10), hide_index=True, use_container_width=True)

        # Q7
        st.subheader('High channel views')
        st.dataframe(stConn.query(
            'SELECT channel_name AS "Channel Name", channel_views AS "Channel Views" FROM ytChannel ORDER BY channel_views DESC;').head(10), hide_index=True, use_container_width=True)

        # Q8
        stDFQ1 = stConn.query(
            '''
                SELECT ytCh.channel_name AS "Channel Name", ytV.video_publishedAt AS "Video Published"
                FROM ((ytVideo ytV
                INNER JOIN ytPlaylist ytP ON ytV.playlist_id = ytP.playlist_id)
                INNER JOIN ytChannel ytCh ON ytP.channel_id = ytCh.channel_id) WHERE YEAR(video_publishedAt) LIKE "%2022";
                    ''',
            ttl=60
        )
        st.subheader('Channels published video on 2022')
        st.dataframe(stDFQ1.sort_values(
            'Channel Name').head(10), hide_index=True, use_container_width=True)

        # Q9
        stDFQ1 = stConn.query(
            '''
                SELECT ytCh.channel_name AS "Channel Name", 
                SEC_TO_TIME(ROUND(AVG(TIME_TO_SEC(ytV.video_duration)))) AS "Average Duration"
                FROM ((ytVideo ytV
                INNER JOIN ytPlaylist ytP ON ytV.playlist_id = ytP.playlist_id)
                INNER JOIN ytChannel ytCh ON ytP.channel_id = ytCh.channel_id) 
                GROUP BY ytCh.channel_name;
                    ''',
            ttl=60
        )
        stDFQ1['Average Duration'] = stDFQ1['Average Duration'].astype(str)
        st.subheader('Avg video duration by channel')
        st.dataframe(stDFQ1.sort_values(
            'Average Duration', ascending=False).head(10), hide_index=True, use_container_width=True)


if __name__ == "__main__":
    main()
