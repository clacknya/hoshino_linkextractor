#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import nonebot

from hoshino import Service

sv = Service('链接提取器', visible=True, enable_on_default=False)

@sv.on_notice('group_upload')
async def group_upload(session: nonebot.NoticeSession):
	self_info = await session.bot.get_login_info()
	chain = [
		nonebot.MessageSegment.node_custom(
			user_id=session.ctx.self_id,
			nickname=self_info['nickname'],
			content=f"{session.ctx.user_id} 上传了文件 {session.ctx.file.get('name')}",
		),
		nonebot.MessageSegment.node_custom(
			user_id=session.ctx.self_id,
			nickname=self_info['nickname'],
			content=session.ctx.file.get('url'),
		),
	]
	for node in chain:
		node['data']['name'] = self_info['nickname']
	await session.bot.send_group_forward_msg(group_id=session.ctx.group_id, messages=chain)

@sv.on_message('group')
async def antiminiapp(bot, ev: nonebot.message.CQEvent):
	if ev.detail_type == 'guild':
		return
	self_info = await bot.get_login_info()
	for msg in ev.message:
		if msg.get('type') == 'video':
			chain = [
				nonebot.MessageSegment.node_custom(
					user_id=ev.self_id,
					nickname=self_info['nickname'],
					content=f"{ev.user_id} 发送了视频",
				),
				nonebot.MessageSegment.node_custom(
					user_id=ev.self_id,
					nickname=self_info['nickname'],
					content=nonebot.message.unescape(msg['data'].get('url', '')),
				),
			]
			for node in chain:
				node['data']['name'] = self_info['nickname']
			await bot.send_group_forward_msg(group_id=ev.group_id, messages=chain)
