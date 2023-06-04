async def check_post_owner(feedbacks, fid, touristId):
    return feedbacks[fid].touirst_id == touristId
