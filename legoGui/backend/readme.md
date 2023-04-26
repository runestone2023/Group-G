# Group-G

## Names

Dinh Ngoc Khue, Vu Pham Viet Honag, Dinh Huu Dai, Amir Masoud Baghi, Viktor Björk, Yi-Jun Tang, Carl Willman, and Aravind Srisai Kishore.

## Project board

[Github project board](https://github.com/orgs/runestone2023/projects/5)

## IDE setup

[VS Code](https://code.visualstudio.com) as the IDE for the robots, UI, and server

## Extensions

[LEGO® MINDSTORMS® EV3 MicroPython](https://marketplace.visualstudio.com/items?itemName=lego-education.ev3-micropython) for programming the Lego EV3 robots

[Live Share](https://marketplace.visualstudio.com/items?itemName=MS-vsliveshare.vsliveshare) for pair programming

## Communication

Discord and GitHub Projects

## Running the project

`make init` to install dependencies, `make server` to run the server, and `make
client` to run the client.

## To configure the frontend

you must have nodejs and npm installed to run a react project.
cd inside the frontend folder and type `npm install` to install the dependecices , then type `npm start` to start the frontend on localhost:3000.

in another terminal go inside the backend folder and run `uvicorn server:app --reload` , it will run on localhost:8000
