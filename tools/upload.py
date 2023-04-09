from vk_api import VkUpload
from . import config


class Uploaders():
	def __init__(self, session):
		self.uploader = VkUpload(session)

	def upload_photo(self, images: list):
		attachments = []
		for image in images:
			upload_image = self.uploader.photo_wall(photos = image, group_id=config.owner_id)[0]
			attachments.append("photo{}_{}".format(upload_image['owner_id'], upload_image['id']))

		return ",".join(attachments)

	def upload_video(self, videos: list):
		attachments = []
		for video in videos:
			upload_video = self.uploader.video(video_file = video, group_id=config.owner_id)
			attachments.append("video{}_{}".format(upload_video['owner_id'], upload_video['video_id']))

		return ",".join(attachments)