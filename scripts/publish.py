#!/usr/bin/env python3
"""Publish this committed release to dimkadimon/No3InLine using your local GitHub CLI login.
Default: inspect only. --apply: create public only if absent; otherwise merge into the existing default branch.
No forced push, visibility change, automatic conflict resolution, token argument or token storage.
"""
import argparse, json, os, re, subprocess, sys, tempfile
from pathlib import Path
R=Path(__file__).resolve().parents[1];REPO='dimkadimon/No3InLine';HOST='github.com';URL=f'https://{HOST}/{REPO}.git';ENV={**os.environ,'GIT_TERMINAL_PROMPT':'0','GH_PROMPT_DISABLED':'1','GH_HOST':HOST}
def run(cmd,cwd=R,ok=True):
    z=subprocess.run(cmd,cwd=cwd,env=ENV,text=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    if ok and z.returncode:raise SystemExit(z.stderr.strip() or z.stdout.strip() or f'{cmd[0]} failed')
    return z
def git(*args,cwd=R,ok=True):return run(['git','-c','credential.helper=','-c','credential.helper=!gh auth git-credential',*args],cwd=cwd,ok=ok)
def api(endpoint,ok=True):return run(['gh','api','--hostname',HOST,endpoint],ok=ok)
def metadata(ok=True):
    z=api('repos/'+REPO,ok=False)
    if z.returncode==0:return json.loads(z.stdout)
    if not ok and re.search(r'\bHTTP 404\b',z.stderr):return None
    raise SystemExit('Cannot inspect the target repository safely: '+z.stderr.strip())
def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--apply',action='store_true',help='perform the non-force publication; without this flag there are no remote writes');a=p.parse_args()
    auth=api('user',ok=False)
    if auth.returncode:raise SystemExit('No usable GitHub CLI login. On your own machine run: gh auth login --hostname github.com --web. Do not paste a token into this repository.')
    who=json.loads(auth.stdout)['login'];target=metadata(False)
    if target is None and who.casefold()!=REPO.split('/')[0].casefold():raise SystemExit('A 404 is ambiguous for this account. Refusing to create a repository outside the authenticated owner account.')
    if target and (target['full_name'].casefold()!=REPO.casefold() or not target.get('permissions',{}).get('push')):raise SystemExit('Repository identity or write permission could not be confirmed.')
    if git('status','--porcelain','--untracked-files=no').stdout:raise SystemExit('Commit or set aside tracked local changes first; nothing was uploaded.')
    head=git('rev-parse','--verify','HEAD^{commit}').stdout.strip()
    print(f'Authenticated as {who}; local commit {head}.',flush=True)
    if target:print(f'Existing {target["visibility"]} repository: default branch {target["default_branch"]}. Visibility will not change.',flush=True)
    else:print('Authenticated lookup returned 404. Creation, if permitted and the name is free, will request a PUBLIC repository.',flush=True)
    if not a.apply:print('Inspection only. Run with --apply to publish.');return
    if target is None:
        run(['gh','repo','create',REPO,'--public']);target=metadata()
        if target['full_name'].casefold()!=REPO.casefold() or target['visibility']!='public':raise SystemExit('Creation returned unexpected metadata. No push attempted.')
    branch=target.get('default_branch') or 'main';git('check-ref-format','--branch',branch);ref='refs/heads/'+branch
    visible=git('ls-remote',URL).stdout.splitlines();has_default=any(x.split('\t')[-1]==ref for x in visible)
    if visible and not has_default:raise SystemExit('Remote has refs but its default branch was not found; not pushing.')
    with tempfile.TemporaryDirectory() as t:
        d=Path(t)/'integration';git('clone','-q','--no-checkout','--no-hardlinks',str(R),str(d));owner='Arena.ai release agent';mail='release@no3inline.invalid'
        if has_default:
            git('fetch','--no-tags',URL,ref,cwd=d);upstream=git('rev-parse','FETCH_HEAD',cwd=d).stdout.strip();git('checkout','--detach',upstream,cwd=d)
            z=git('-c','user.name='+owner,'-c','user.email='+mail,'merge','--no-edit','--allow-unrelated-histories',head,cwd=d,ok=False)
            if z.returncode:raise SystemExit('Integration requires manual conflict resolution; the existing branch has not been changed.\n'+z.stdout.strip()+'\n'+z.stderr.strip())
            git('merge-base','--is-ancestor',upstream,'HEAD',cwd=d)
        else:git('checkout','--detach',head,cwd=d)
        published=git('rev-parse','HEAD',cwd=d).stdout.strip();git('merge-base','--is-ancestor',head,published,cwd=d)
        git('push',URL,f'{published}:{ref}',cwd=d)  # Git refuses a concurrent non-fast-forward update.
    after=git('ls-remote',URL,ref).stdout.split()
    if not after or after[0]!=published:raise SystemExit('Remote branch tip could not be confirmed; inspect the remote before retrying.')
    print(f'Confirmed {REPO} on {branch}: https://{HOST}/{REPO}/commit/{published}')
if __name__=='__main__':main()
