file = open("list.txt", 'r')
prev_file_content = file.readlines()
file.close()

print(prev_file_content)
prev_file_content.pop(0)
print(prev_file_content)

file = open("list.txt", 'w', encoding='utf-8')
file.write("")
file.close()

for i in prev_file_content:
    file = open("list.txt", 'r')
    prev = file.read()
    file.close()
    file = open("list.txt", 'w', encoding='utf-8')
    file.write(prev+i)
    file.close()