import cascade

session = cascade.Session('TOKEN')

@session.event
async def on_ready():
    invite_code = 'bleed'
    
    try:
        await session.accept_invite(invite_code)
        print(f'✅ Joined server!')
        
    except cascade.CaptchaRequired as e:
        print(f'❌ Captcha required!')
        print(f'   Service: {e.captcha_service}')
        print(f'   Sitekey: {e.captcha_sitekey}')
        print(f'   RQ Data: {e.captcha_rqdata}')
        print(f'   RQ Token: {e.captcha_rqtoken}')
        print(f'   Session ID: {e.captcha_session_id}')
        print()
        print('You can solve this manually or use a free AI solver like:')
        print('- https://github.com/ScremerMemer/Hcaptcha-Solver (free AI solver)')
        print('- https://github.com/korolossamy/hcaptcha-ai-solver (free)')
        print()
        print('Then retry with:')
        print(f'  await session.rest.accept_invite("{invite_code}", captcha_key="solved_key")')
        
    except cascade.Forbidden as e:
        print(f'❌ Access denied: {e.text}')
        
    except cascade.NotFound as e:
        print(f'❌ Not found: {e.text}')
        
    except cascade.HTTPException as e:
        print(f'❌ HTTP error {e.status}: {e.text}')

session.run()
