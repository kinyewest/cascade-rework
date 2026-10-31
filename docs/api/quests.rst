Quests
======

The quests module provides a safe, high-level interface to Discord's quest system.

Overview
--------

Discord quests reward users for completing tasks like playing games, watching streams, or joining voice channels. Cascade's ``QuestClient`` handles enrollment, heartbeats, and reward claiming with built-in safety measures to avoid detection.

Quick Start
-----------

.. code-block:: python

   from cascade import Session

   session = Session('TOKEN')

   @session.event
   async def on_ready():
       quests = await session.quests.get_quests()
       for quest in quests:
           print(f'{quest.config.messages.game_title}: {quest.config.reward_code.sku_id}')
       
       active = await session.quests.get_active_quests()
       for quest in active:
           await session.quests.run_heartbeat_loop(quest.id)

   session.run()

QuestClient
-----------

The ``QuestClient`` is accessed via ``session.quests`` (lazy-initialized).

Fetching Quests
~~~~~~~~~~~~~~~

.. code-block:: python

   all_quests = await session.quests.get_quests()
   claimed = await session.quests.get_claimed_quests()
   quest = await session.quests.get_quest(quest_id)
   
   active = await session.quests.get_active_quests()
   completable = await session.quests.get_completable_quests()

Enrolling & Claiming
~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   await session.quests.enroll(quest_id)
   await session.quests.claim_reward(quest_id)
   code = await session.quests.get_reward_code(quest_id)
   print(f'Reward code: {code.code}')

Heartbeats
~~~~~~~~~~

**For stream/game quests:**

.. code-block:: python

   await session.quests.run_heartbeat_loop(quest_id)

Safe loop with 55-65s intervals, jitter, and automatic terminal heartbeat on completion.

**For video quests:**

.. code-block:: python

   await session.quests.run_video_quest(quest_id, total_duration_secs=120)

Sends progress heartbeats every 5-10 seconds with appropriate jitter.

**Manual heartbeat:**

.. code-block:: python

   from cascade.quests import QuestTaskHeartbeat
   
   heartbeat = QuestTaskHeartbeat(
       stream_key='application:1234567890',
       terminal=False
   )
   await session.quests.send_heartbeat(quest_id, [heartbeat])

Console Quests
~~~~~~~~~~~~~~

.. code-block:: python

   await session.quests.start_console_quest(quest_id, sku_id)
   await asyncio.sleep(3600)
   await session.quests.stop_console_quest(quest_id)

Other Methods
~~~~~~~~~~~~~

.. code-block:: python

   await session.quests.dismiss_content(content_type='quest', content_id=quest_id)
   placement = await session.quests.get_quest_placement()
   apps = await session.quests.get_detectable_applications()

Quest
-----

.. list-table::
   :header-rows: 1
   :widths: 25 75

   * - Attribute
     - Description
   * - ``id``
     - Quest ID
   * - ``config``
     - :class:`QuestConfig` object
   * - ``user_status``
     - :class:`QuestUserStatus` or ``None``

QuestConfig
-----------

.. list-table::
   :header-rows: 1
   :widths: 25 75

   * - Attribute
     - Description
   * - ``config_id``
     - Config ID
   * - ``config_version``
     - Version integer
   * - ``application_id``
     - Application ID
   * - ``application_name``
     - Application name
   * - ``expires_at``
     - Expiration timestamp
   * - ``reward_code``
     - :class:`QuestReward` object
   * - ``tasks``
     - List of task progress dicts
   * - ``in_game_only``
     - Whether requires in-game activity
   * - ``messages``
     - Dict with ``game_title``, ``game_publisher``, etc.
   * - ``targeting``
     - Targeting dict
   * - ``quest_rewards``
     - List of reward dicts

QuestUserStatus
---------------

.. list-table::
   :header-rows: 1
   :widths: 25 75

   * - Attribute
     - Description
   * - ``enrolled_at``
     - Enrollment timestamp
   * - ``completed_at``
     - Completion timestamp or ``None``
   * - ``claimed_at``
     - Claim timestamp or ``None``
   * - ``dismissed_at``
     - Dismiss timestamp or ``None``
   * - ``progress``
     - Dict of task ID to :class:`QuestTaskProgress`
   * - ``last_stream_heartbeat_at``
     - Last heartbeat timestamp

QuestTaskProgress
-----------------

.. list-table::
   :header-rows: 1
   :widths: 25 75

   * - Attribute
     - Description
   * - ``task_id``
     - Task ID
   * - ``completed_at``
     - Completion timestamp or ``None``
   * - ``progress``
     - Current progress value

QuestReward
-----------

.. list-table::
   :header-rows: 1
   :widths: 25 75

   * - Attribute
     - Description
   * - ``sku_id``
     - SKU ID
   * - ``approximate_count``
     - Approximate reward count
   * - ``reward_type``
     - :class:`QuestRewardType` enum
   * - ``assignment_method``
     - :class:`QuestRewardAssignmentMethod` enum

ClaimedQuest
------------

.. list-table::
   :header-rows: 1
   :widths: 25 75

   * - Attribute
     - Description
   * - ``quest_id``
     - Quest ID
   * - ``claimed_at``
     - Claim timestamp
   * - ``code``
     - Reward code string

Enums
-----

**QuestTaskType**

``PLAY_ON_DESKTOP``, ``VIDEO``, ``QUEST_BAR``, ``VOICE_CHANNEL``

**QuestRewardType**

``AVATAR_DECORATION``, ``PROFILE_EFFECT``, ``IN_GAME``

**QuestRewardAssignmentMethod**

``AUTOMATIC``, ``CODE``

**QuestPlatform**

``ANY``, ``DESKTOP``, ``MOBILE``

**QuestContentType**

``quest``, ``quest_bar``

Safety Notes
------------

Cascade's quest implementation includes safety measures:

- Heartbeats use 55-65 second intervals with jitter (never faster)
- User-Agent includes ``Electron/`` component required by Discord
- ``run_heartbeat_loop()`` sends terminal heartbeat on completion
- No burst heartbeats or suspicious patterns

Always use the high-level methods (``run_heartbeat_loop``, ``run_video_quest``) rather than manual heartbeat construction.
