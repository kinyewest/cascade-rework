import cascade

session = cascade.Session('TOKEN')

@session.event
async def on_ready():
    invite_code = 'bleed'
    
    try:
        await session.accept_invite(invite_code)
        print(f'✅ Joined server!')
        
    except cascade.CaptchaRequired as e:
        print(f'🔒 Captcha required! Solving with PyPasser...')
        
        try:
            from pypasser.captcha import hcaptcha
            
            result = hcaptcha.solve(
                site_key=e.captcha_sitekey,
                domain='https://discord.com',
                rqdata=e.captcha_rqdata,
            )
            
            if result.is_solved:
                print(f'✅ Captcha solved! Token: {result.response_token[:50]}...')
                
                captcha_payload = {
                    'captcha_key': result.response_token,
                    'captcha_rqtoken': e.captcha_rqtoken,
                }
                
                data = await session.rest.accept_invite(invite_code, json=captcha_payload)
                print(f'✅ Successfully joined server!')
            else:
                print(f'❌ Failed to solve captcha: {result.error_code}')
                
        except ImportError:
            print('❌ PyPasser not installed!')
            print('   Install it: pip install "PyPasser[all]"')
            print('   GitHub: https://github.com/xHossein/PyPasser')
        except Exception as solver_error:
            print(f'❌ Solver error: {solver_error}')
            
    except cascade.Forbidden as e:
        print(f'❌ Access denied: {e.text}')
        
    except cascade.NotFound as e:
        print(f'❌ Invite not found: {e.text}')

session.run()
