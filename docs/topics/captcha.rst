Captcha Handling
================

Some Discord servers require captcha verification when joining via invite.

Detecting Captcha
-----------------

When a captcha is required, cascade raises ``CaptchaRequired``:

.. code-block:: python

   import cascade

   session = cascade.Session('TOKEN')

   @session.event
   async def on_ready():
       try:
           await session.accept_invite('invite_code')
       except cascade.CaptchaRequired as e:
           print(f'Captcha required!')
           print(f'Service: {e.captcha_service}')        # 'hcaptcha'
           print(f'Sitekey: {e.captcha_sitekey}')
           print(f'RQ Data: {e.captcha_rqdata}')
           print(f'RQ Token: {e.captcha_rqtoken}')

   session.run()

Solving with PyPasser (Free)
-----------------------------

`PyPasser <https://github.com/xHossein/PyPasser>`_ is a free, open-source captcha solver.

Install:

.. code-block:: bash

   pip install "PyPasser[all]"

Example:

.. code-block:: python

   from pypasser.captcha import hcaptcha

   @session.event
   async def on_ready():
       try:
           await session.accept_invite('code')
       except cascade.CaptchaRequired as e:
           result = hcaptcha.solve(
               site_key=e.captcha_sitekey,
               domain='https://discord.com',
               rqdata=e.captcha_rqdata,
           )
           
           if result.is_solved:
               captcha_payload = {
                   'captcha_key': result.response_token,
                   'captcha_rqtoken': e.captcha_rqtoken,
               }
               await session.rest.accept_invite('code', json=captcha_payload)

Manual Solving
--------------

You can also solve captchas manually:

1. Catch the ``CaptchaRequired`` exception
2. Present the captcha to the user (browser iframe with sitekey)
3. Get the solved token from user
4. Retry with ``captcha_key`` in payload

Example:

.. code-block:: python

   try:
       await session.accept_invite('code')
   except cascade.CaptchaRequired as e:
       print(f'Solve manually: https://discord.com/channels/@me')
       solved_token = input('Enter solved captcha token: ')
       
       captcha_payload = {
           'captcha_key': solved_token,
           'captcha_rqtoken': e.captcha_rqtoken,
       }
       await session.rest.accept_invite('code', json=captcha_payload)

Paid Services
-------------

If you prefer paid services:

- `2captcha <https://2captcha.com>`_ - $1-3 per 1000 solves
- `Anti-Captcha <https://anti-captcha.com>`_ - $0.50-2 per 1000 solves
- `CapSolver <https://capsolver.com>`_ - $0.80 per 1000 solves

These services provide APIs that return solved tokens. Use them the same way as PyPasser.

Exception Hierarchy
-------------------

.. code-block:: text

   CascadeException
   └── HTTPException
       ├── Forbidden (403)
       ├── NotFound (404)
       └── CaptchaRequired (400 with captcha_key field)

All HTTP errors include:

- ``status`` - HTTP status code
- ``text`` - Error response body
- ``response`` - Original aiohttp response object

``CaptchaRequired`` additionally includes:

- ``captcha_service`` - ``'hcaptcha'``
- ``captcha_sitekey`` - Site key for solver
- ``captcha_rqdata`` - Request data
- ``captcha_rqtoken`` - Request token
- ``captcha_session_id`` - Session ID
