robots = """User-agent: *
Allow: /

# 单页站，没有需要屏蔽的路径
"""
open("robots.txt","w",encoding="utf-8").write(robots)
print("robots.txt 已写入")
