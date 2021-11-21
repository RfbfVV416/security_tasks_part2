This is an example of a basic injection into the portable executable file
by adding a new section.

## Algorithm
1 Search of executable file in folder </br>
2 Resize the executable file </br>
3 Add the new section header </br>
4 Modify the main headers </br>
5 Inject the shellcode in the new section

## Demonstration
Let's create a folder with some number of files.
Some of them will be executable.
![image](https://user-images.githubusercontent.com/62764458/142764332-a623a0e2-453b-47ab-9214-93550456ae19.png)

Before the injection we can observe the ```Target.exe``` via CFF Explorer
and pay attention to its' size and sections.
![image](https://user-images.githubusercontent.com/62764458/142765121-0c65510c-4484-4d75-bf93-9851854d8afc.png)
![image](https://user-images.githubusercontent.com/62764458/142765164-4328483e-365f-4c69-a5fa-ebee70679f6e.png)

After the execution of the ```main.py``` we are able to see the details
of injection.
![image](https://user-images.githubusercontent.com/62764458/142765350-992d9b68-5447-4fe0-9223-5d9f5fad7a2f.png)

After the injection file size changed
and a new ```.test``` section appeared.
![image](https://user-images.githubusercontent.com/62764458/142765570-27f5ea9c-fac9-41eb-85c9-49081d97f2e6.png)
![image](https://user-images.githubusercontent.com/62764458/142765603-a824c32b-cd23-4405-b202-fd52f930235e.png)

