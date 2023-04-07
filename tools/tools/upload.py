from vk_api import VkUpload
from . import config

def _get_uploader(session) -> VkUpload:
	return VkUpload(session)

def _upload_photo(uploader: VkUpload, images: list) -> str:
	attachments = []
	for image in images:
		upload_image = uploader.photo_wall(photos = image, group_id=config.owner_id)[0]
		attachments.append("photo{}_{}".format(upload_image['owner_id'], upload_image['id']))

	return ",".join(attachments)

def _upload_video(uploader: VkUpload, videos: list) -> str:
	attachments = []
	for video in videos:
		upload_video = uploader.video(video_file = video, group_id=config.owner_id)
		attachments.append("video{}_{}".format(upload_video['owner_id'], upload_video['video_id']))

	return ",".join(attachments)