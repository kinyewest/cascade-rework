# Changelog

All notable changes to this project will be documented here.

Format: `## [version] - YYYY-MM-DD`

---

## [0.4.1] - 2026-10-20

Same as 0.4.0 (republish due to tag conflict).

## [0.4.0] - 2026-10-20

### Added
- **Quests module**: Full quest system support with `QuestClient`, `Quest`, `QuestConfig`, `QuestUserStatus`, `QuestTaskProgress`, `QuestReward`, `ClaimedQuest`
  - `session.quests` property for lazy-initialized quest client
  - Safe heartbeat loops with 55-65s intervals and jitter
  - `run_heartbeat_loop()`, `run_video_quest()` for automated quest completion
  - Quest enrollment, claim, reward code retrieval
  - Console quest support
- **Attachment entity**: `Attachment` object with `is_image()`, `is_video()`, `is_audio()` methods
- **Forum support**: `ForumChannel`, `ForumPost`, `ForumTag` entities
- **Integration entity**: `Integration`, `IntegrationAccount`, `IntegrationApplication`
- **Guild preview**: `GuildPreview` entity and `fetch_guild_preview()` method
- **Voice regions**: `VoiceRegion` entity and `fetch_voice_regions()` method
- **Message search**: `MessageSearchResult` entity for search results with context
- **Note entity**: `Note` with `edit()` and `delete()` methods
- **MessageBuilder**: Fluent message builder with `content()`, `embed()`, `component()`, `reply()`, `suppress_mentions()`, `tts()`, `suppress_embeds()`, `ephemeral()`, `nonce()`, `sticker()` methods
- **AllowedMentions**: Mention control with `.none()`, `.all()` factory methods
- **Rich guild methods**: 15+ new `Guild` methods including `fetch_channels()`, `fetch_member()`, `fetch_bans()`, `fetch_audit_log()`, `fetch_templates()`, `fetch_onboarding()`, `fetch_welcome_screen()`, `fetch_scheduled_events()`, `fetch_invites()`, `fetch_webhooks()`, `fetch_stickers()`, `fetch_emojis()`, `fetch_roles()`, `edit()`
- **Rich member methods**: `edit()`, `set_nickname()`, `add_role()`, `remove_role()`, `kick()`, `ban()`, `timeout()`, `remove_timeout()`, `send()`, `fetch_profile()`
- **30+ new REST endpoints**: `bulk_ban()`, `recent_mentions()`, `notes CRUD`, `hypesquad house`, `proto settings`, `join requests`, `member verification`, `greet()`, `forum posts`, `voice channel status`, and more
- **Gateway events**: `GUILD_BAN_ADD`, `GUILD_BAN_REMOVE`, `GUILD_EMOJIS_UPDATE`, `GUILD_INTEGRATIONS_UPDATE`, `CHANNEL_PINS_UPDATE`, `GUILD_MEMBERS_CHUNK`, `THREAD_LIST_SYNC`, `THREAD_MEMBERS_UPDATE`, `SESSIONS_REPLACE`, `VOICE_CHANNEL_STATUS_UPDATE`, `MESSAGE_REACTION_REMOVE_EMOJI`
- Message attachments now parse as `Attachment` objects (was raw dicts)
- `on_presence_update` now dispatches `Presence` entity (was raw dict)
- `on_user_update` now dispatches `ClientUser` (was dict)
- `on_reaction_add/remove` now dispatch `Reaction` entity (was dict)
- **Webhook execution**: `webhook.send()`, `webhook.edit_message()`, `webhook.delete_message()`, `webhook.fetch_message()` methods
- **Thread management**: `channel.create_thread()`, `channel.add_member()`, `channel.remove_member()`, `channel.join()`, `channel.leave()` methods
- **Bulk message operations**: `channel.bulk_delete(message_ids)` — delete up to 100 messages at once
- **Channel permissions**: `channel.edit_permissions()`, `channel.delete_permissions()` for managing permission overwrites
- **Guild widget**: `guild.fetch_widget()`, `guild.fetch_widget_settings()`, `guild.edit_widget()` methods
- **Guild vanity URL**: `guild.fetch_vanity_url()` method
- **Voice regions**: `session.fetch_voice_regions()` returns list of `VoiceRegion` objects
- **Read all shortcut**: `session.ack_all()` — mark all guilds as read

### Changed
- **Discord version strings updated** (critical for avoiding detection):
  - Electron: `42.0.0` (unchanged)
  - Chrome: `148.0.0.0` (was `136.0.0.0`) — Chromium 148 in Electron 42
  - Desktop app version (Windows): `1.0.9266` (was `1.0.9262`)
  - Desktop app version (macOS): `0.0.320` (unchanged)
  - Desktop app version (Linux): `0.0.72` (unchanged)
  - `client_build_number`: `635180` (unchanged)
  - `Sec-Ch-Ua`: Updated to Chrome 148
- `fetch_read_states()` now uses correct `/users/@me/read-states/v2` endpoint
- All version strings updated in `rest.py`, `shard.py`, and `spoof/platforms.py`
- `Webhook.from_dict()` now accepts optional `session` parameter

### Fixed
- Removed `br` (Brotli) from `Accept-Encoding` header — was causing 400 errors
- Fixed `Message.clear_reactions()` missing `await`
- Fixed missing `datetime` import in `message.py`

### Documentation
- Added complete quest system documentation (`docs/api/quests.rst`)
- Added `Attachment`, `ForumChannel/Post/Tag`, `Integration`, `GuildPreview`, `VoiceRegion`, `Note`, `MessageSearchResult` to entities docs
- Added `MessageBuilder` and `AllowedMentions` to utils docs
- Updated index with quests section

## [0.3.1] - 2026-10-20

### Fixed
- Gateway send queue — all outgoing messages serialized, none drop during reconnect
- Proper WebSocket close code handling — 4004/4014 fatal and stop immediately, others resume or re-identify
- Guild stubs from READY payload now cache correctly (`unavailable: true` no longer throws)
- `GUILD_CREATE` after READY updates unavailable stubs and fires `on_guild_available` instead of `on_guild_join`
- Zombie detection — 2 missed heartbeat acks triggers reconnect
- Exponential backoff on reconnect capped at 60s, resets on successful ack
- Heartbeat loop cancels cleanly on reconnect

### Added
- `on_guild_available` event when an unavailable guild becomes available
- `on_guild_update` event
- Thread events: `on_thread_create`, `on_thread_update`, `on_thread_delete`
- Member events: `on_member_join`, `on_member_remove`, `on_member_update`
- Role events: `on_role_create`, `on_role_update`, `on_role_delete`
- Reaction events: `on_reaction_add`, `on_reaction_remove`, `on_reaction_clear`
- `on_webhooks_update`, `on_audit_log_entry`, `on_voice_server_update`
- `GatewayShard.update_presence()` method

---

## [0.3.0] - 2026-10-20

### Added
- **Scheduled events** - `ScheduledEvent` entity with create/edit/delete/start/complete/cancel/fetch users. Gateway events `on_scheduled_event_create/update/delete`
- **Stage instances** - `StageInstance` with create/edit/delete/request_to_speak. Gateway `on_stage_create/update/delete`
- **Polls** - `Poll`, `PollBuilder`, `PollAnswer`. Vote, remove vote, end poll, fetch voters. Gateway `on_poll_vote_add/remove`
- **Stickers** - `Sticker` entity with edit/delete. Full guild sticker management endpoints + standard packs
- **Soundboard** - `SoundboardSound` with send/edit/delete. Default sounds + guild sounds. `on_soundboard_update`
- **Read states** - `ReadState` entity, `session.fetch_read_states()`, per-channel and guild-wide ack
- **Billing & Nitro** - `Subscription`, `PaymentSource`, `GiftCode`, `PremiumType`. Fetch subscriptions, payment sources, payments, applied boosts, Nitro status, redeem/fetch gift codes, promotions
- **Profile customisation** - `session.set_profile_bio/pronouns/banner/theme_colors()`. Set avatar decoration, theme colors (primary + accent)
- **Invites** - `Invite` entity with full guild/channel metadata. `session.fetch_invite()`, `session.accept_invite()`
- **VoiceStateEntity** - proper typed entity for voice state updates (replaces raw dict dispatch)
- **Expanded gateway events** - `on_relationship_add/remove` now pass `Relationship` entities. Added `on_voice_state_update`, `on_invite_create/delete`, `on_stickers_update`
- **Expanded enums** - `StagePrivacyLevel`, `ScheduledEventStatus/EntityType/PrivacyLevel`, `StickerType/FormatType`, `PremiumType`, `RelationshipType`, `InteractionType` all added to `cascade.types.enums`
- 20+ new REST endpoints across scheduled events, stage instances, polls, stickers, soundboard, billing, profile

### Changed
- `on_relationship_add/remove` now dispatch `Relationship` objects instead of raw dicts
- `on_voice_state_update` now dispatches `VoiceStateEntity` instead of raw dict
- Version bump: `cascade.__version__` is now `'0.3.0'`

---



### Changed
- `pyproject.toml` modernised - SPDX license string, `setuptools>=77`, optional extras (`voice`, `security`), docs/changelog URLs, examples excluded from package
- README rewritten to be minimal - matches discord.py-self style
- Docs switched to Furo theme with Discord-branded dark mode colours

### Added
- Changelog page in documentation
- `Documentation` and `Changelog` links on PyPI

---

## [0.2.0] - 2026-10-20

### Added
- **Device spoofing** - 14 platform presets (desktop, mobile, iOS, Android, VR, Xbox, PlayStation) with automatic X-Super-Properties and User-Agent injection
- **Platform switching at runtime** - `session.set_platform()` hot-swaps properties without reconnecting
- **Voice support** - `VoiceClient`, `VoiceState`, `PCMAudio`, `FFmpegAudio`, `OpusEncoder`
- **Interactions** - `Button`, `SelectMenu`, `TextInput`, `ActionRow`, `Modal`, full `Interaction` response handling
- **Auto-moderation** - `AutoModRule`, `AutoModAction`, `AutoModTriggerMetadata` with keyword/regex/preset/mention-spam triggers
- **Advanced caching** - LRU, LFU, FIFO, TTL strategies; `LayeredCache` (L1/L2/L3); per-entry TTL; eviction callbacks; cache stats
- **Rich presence builder** - `RichActivity` fluent API with assets, timestamps, party, secrets, buttons
- **Security module** - `TokenManager` (masking, validation, user ID extraction, optional AES-256 encryption), `FingerprintRandomizer` (canvas, resolution, timezone, typing/mouse patterns), `SmartRateLimiter` (adaptive delays, bucket tracking)
- **Docs** - Sphinx + Read the Docs setup with full API reference, quickstart, event reference, caching/presence/rate-limit guides

### Changed
- Updated desktop/web Chrome to **136**, Electron to **42**, build number to **635180**
- Updated Android Discord client to **350.6**, iOS to **350.0**
- Cleaned up platform presets - removed duplicates (`quest2`, `quest3`, `ps5`, `windows`, `iphone`, `ipad` kept as aliases only)
- Rewrote `README.md` to be minimal and focused

### Fixed
- `RestClient` now accepts `spoofer` parameter and rebuilds headers/super-properties from it
- `GatewayShard` now reads `spoofer` from session and uses it in `_build_client_properties`

---

## [0.1.0] - 2026-01-18

### Added
- Full Discord Gateway v10 - connect, heartbeat, resume, reconnect, INVALID_SESSION handling
- 120+ REST API endpoints covering users, guilds, channels, messages, roles, webhooks, threads, voice, search, connections, settings, billing, relationships, and more
- Rate limiter with per-bucket tracking and automatic retry
- Entity models - `User`, `ClientUser`, `Guild`, `Channel`, `TextChannel`, `DMChannel`, `VoiceChannel`, `GroupChannel`, `Message`, `Member`, `Role`, `Emoji`, `Presence`, `Webhook`, `Connection`, `UserSettings`, `Application`
- Event dispatcher with `@session.event` decorator and `wait_for` support
- Cache system for guilds, channels, users, messages
- Command framework - `Bot`, `Context`, `@command` decorator with prefix support
- Utilities - `Permission`, `Permissions`, `Intents`, `Snowflake`, `Color`, `MarkdownProcessor`, `TypingIndicator`, `BackoffStrategy`, `Chunker`, `Validator`
- Examples - `basic.py`, `commands.py`, `advanced.py`, `moderation.py`
- MIT license, `pyproject.toml`, `setup.py`, `MANIFEST.in`
