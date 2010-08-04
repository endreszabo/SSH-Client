#!/usr/bin/python -tt

#from paramiko import SSHConfig
from sys import exit, argv

#sshconfig=open("/home/endre/.ssh/config",'rb')

#config=SSHConfig()
#config.parse(sshconfig)
#hosts=[]
#for lines in config._config:
#	hosts.append(lines['host'])

def grepString(pattern, string):
	hb='<'
	he='>'
	if pattern == '':
		return {
			string: {
				'score': 0,
				'hilited': string
			}
		}
	lcString=string.lower()
	lcPattern=pattern.lower()
	if lcString == lcPattern:
		return {
			string: {
				'score': len(string)+2,
				'hilited': hb+string+he
			}
		}
	origString=string
	score=0
	oldpos=-1
	hilited=''
	try:
		if (lcString.index(lcPattern)==0) | \
				(lcString.rindex(lcPattern)+len(lcPattern) == len(lcString)):
			score+=1
	except ValueError:
		pass
	while (len(pattern)>0):
		for i in range(len(pattern),0,-1):
			oldpos=-1
			try:
#				print "oldpos=('%s'.rindex('%s'[:%d])) = %d" % (lcString, lcPattern, i,oldpos)
				oldpos=(lcString.index(lcPattern[:i]))
				if (oldpos >= 0):
#					print "len(pattern)=%d, i=%d, oldpos=%d, score=%02d, pattern='%s', string='%15s', hilite='%15s'" % (len(pattern),i, oldpos, score, pattern, string, hilited)
					hilited=hilited+\
							string[0:oldpos]+\
							hb+\
							string[oldpos:oldpos+i]+\
							he
					if i>1:
						score+=i-1
					#print "i=%d, pattern=%s, partial pattern=%s" % (i,pattern,pattern[i:])
					pattern=pattern[i:]
					lcPattern=pattern.lower()
					oldpos+=i-1
					string=string[oldpos+1:]
					lcString=string.lower()
					break
				elif i == 1:
					return ({origString: None})
			except ValueError:
				if i==1:
					return {
						string: {
							'score': -1,
							'hilited': string
						}
					}
				pass
	hilited=hilited+string
	return {origString: {
		'score': score,
		'hilited': hilited
	}}

for i,iters in enumerate(argv[2:]):
	print '\t'.join([iters,"%s" % grepString(iters,argv[1])])

