import os
cks = os.environ["JD_COOKIE"].split("&")
print(f'检测到{len(cks)}个有效CK，开始写入')
with open('cklist.txt','w') as f:
    for ck in cks:
        f.write(f'{ck}\n')
        #print(ck)
        
