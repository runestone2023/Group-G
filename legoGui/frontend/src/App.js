import React, { useState, useEffect } from "react";
import "./App.css";
import TodoView from "./components/TodoList";
import axios from "axios";
import "bootstrap/dist/css/bootstrap.min.css";

// const express = require("express");
// const cors = require("cors");
// const app = express();
// app.use(
//   cors({
//     origin: "http://localhost:8000/",
//   })
// );

function App() {
  const [todoList, setTodoList] = useState([{}]);
  const [title, setTitle] = useState("");
  const [desc, setDesc] = useState("");
  const [now, setNow] = useState("");

  const startHandler = () => {
    axios
      .post("http://localhost:8000/start/")
      .then((res) => console.log(res.data, res));
  };

  const stopHandler = () => {
    axios
      .post("http://localhost:8000/stop/")
      .then((res) => console.log(res.data, res));
  };

  return (
    <div
      className="App list-group-item  justify-content-center align-items-center mx-auto"
      style={{
        width: "400px",
        backgroundColor: "white",
        marginTop: "15px",
      }}
    >
      <h1
        className="card text-white bg-primary mb-1"
        stylename="max-width: 20rem;"
      >
        Robot Controller
      </h1>
      <h6 className="card text-white bg-primary mb-3">
        FASTAPI - React - LegoEv3
      </h6>
      <div className="card-body">
        <h5 className="card text-white bg-dark mb-3">Select option</h5>
        <span className="card-text">
          <button
            className="btn btn-outline-primary mx-2 mb-3"
            style={{ borderRadius: "50px", fontWeight: "bold" }}
            onClick={startHandler}
          >
            Start Robot
          </button>

          <button
            className="btn btn-outline-primary mx-2 mb-3"
            style={{ borderRadius: "50px", fontWeight: "bold" }}
            onClick={stopHandler}
          >
            Stop Robot
          </button>
        </span>
        <h5 className="card text-white bg-dark mb-3">Your Tasks</h5>
        {/* <div>{currentState}</div> */}
      </div>
      <h6 className="card text-dark bg-warning py-1 mb-0">
        RuneStone Group G&copy;
      </h6>
    </div>
  );
}

export default App;
