import React, { useState, useEffect } from "react";
import "./App.css";
import axios from "axios";
import "bootstrap/dist/css/bootstrap.min.css";
import {
  Container,
  Row,
  Col,
  Button,
  Alert,
  Breadcrumb,
  Card,
  Form,
} from "react-bootstrap";

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

  const fetchClientHandler = () => {
    axios
      .get("http://localhost:8000/clients/")
      .then((res) => console.log(res.data));
  };

  const moveForwardHandler = () => {
    axios.post("http://localhost:8000/clients/0/move", {
      speed: 0,
    });
  };

  const moveBackHandler = () => {
    axios.post("http://localhost:8000/<move back  api call>/", {
      // The data format
    });
  };

  const moveLeftHandler = () => {
    axios.post("http://localhost:8000/<move left  api call>/", {
      // The data format
    });
  };

  const moveRightHandler = () => {
    axios.post("http://localhost:8000/<move right  api call>/", {
      // The data format
    });
  };

  return (
    <>
      <nav className="navbar navbar-dark bg-primary mb-3">RuneStone GroupG</nav>

      <Container className="container-fluid mb-2 w-50 p-3">
        <div className="row">
          {/* Robot Selection Panel */}
          <div className="col-sm">
            <Card className="border border-primary">
              <p>Enable</p>
              <button
                type="button"
                className="btn btn-primary btn-outline-danger my-3 btn-lg"
                style={{
                  color: "white",
                }}
                onClick={fetchClientHandler}
              >
                Fetch
              </button>
              <div class="form-check">
                <input
                  class="form-check-input"
                  type="radio"
                  name="flexRadioDefault"
                  id="flexRadioDefault1"
                />
                <label class="form-check-label" for="flexRadioDefault1">
                  Robot 1
                </label>
              </div>
              <div class="form-check">
                <input
                  class="form-check-input"
                  type="radio"
                  name="flexRadioDefault"
                  id="flexRadioDefault2"
                  checked
                />
                <label class="form-check-label" for="flexRadioDefault2">
                  Robot 2
                </label>
              </div>
              <div class="form-check">
                <input
                  class="form-check-input"
                  type="radio"
                  name="flexRadioDefault"
                  id="flexRadioDefault3"
                  checked
                />
                <label class="form-check-label" for="flexRadioDefault3">
                  Robot 3
                </label>
              </div>
            </Card>
          </div>

          {/* Power Mode */}
          <div className="col-sm">
            <Card className="border border-primary">
              Power
              <div
                className="btn-group"
                role="group"
                aria-label="Basic example"
              >
                <button
                  type="button"
                  className="btn btn-primary btn-outline-danger mx-1 btn-lg"
                  style={{
                    color: "white",
                  }}
                  onClick={startHandler}
                >
                  Turn On
                </button>
                <button
                  type="button"
                  className="btn btn-primary btn-outline-danger mx-1 btn-lg"
                  style={{
                    color: "white",
                  }}
                  onClick={stopHandler}
                >
                  Turn Off
                </button>
              </div>
            </Card>
          </div>
        </div>
      </Container>

      <Container className="container-fluid">
        <div className="row">
          {/* Movement Control */}
          <div className="col-sm">
            <Card className="border border-primary">
              Controls
              <div
                className="btn-group"
                role="group"
                aria-label="Basic example"
              >
                <button
                  type="button"
                  className="btn btn-primary btn-outline-danger mx-1 btn-lg"
                  style={{
                    color: "white",
                  }}
                  onClick={moveLeftHandler}
                >
                  Left
                </button>
                <div className="btn-group-vertical">
                  <button
                    type="button"
                    className="btn btn-primary btn-outline-danger my-3 btn-lg"
                    style={{
                      color: "white",
                    }}
                    onClick={moveForwardHandler}
                  >
                    Forward
                  </button>
                  <button
                    type="button"
                    className="btn btn-primary btn-outline-danger my-3 btn-lg"
                    style={{
                      color: "white",
                    }}
                    onClick={moveBackHandler}
                  >
                    Back
                  </button>
                </div>
                <button
                  type="button"
                  className="btn btn-primary btn-outline-danger mx-1 btn-lg"
                  style={{
                    color: "white",
                  }}
                  onClick={moveRightHandler}
                >
                  Right
                </button>
              </div>
            </Card>
          </div>

          {/* Rotate Section */}
          <div className="col-sm">
            <Card className="border border-primary">
              Controls
              <div
                className="btn-group"
                role="group"
                aria-label="Basic example"
              >
                <button
                  type="button"
                  className="btn btn-primary btn-outline-danger mx-1 btn-lg"
                  style={{
                    color: "white",
                  }}
                >
                  Rotate Left
                </button>
                <div className="btn-group-vertical">
                  <button
                    type="button"
                    className="btn btn-primary btn-outline-danger my-3 btn-lg"
                    style={{
                      color: "white",
                    }}
                  >
                    Claw On
                  </button>
                  <button
                    type="button"
                    className="btn btn-primary btn-outline-danger my-3 btn-lg"
                    style={{
                      color: "white",
                    }}
                  >
                    Claw Off
                  </button>
                </div>
                <button
                  type="button"
                  className="btn btn-primary btn-outline-danger mx-1 btn-lg"
                  style={{
                    color: "white",
                  }}
                >
                  Rotate Right
                </button>
              </div>
            </Card>
          </div>
          {/* Liive Stream */}
          <div className="col-sm">
            <Card className="border border-primary">
              Youtube Live
              <div className="embed-responsive embed-responsive-1by1">
                <iframe
                  className="embed-responsive-item"
                  // src="https://www.youtube.com/embed/zpOULjyy-n8?rel=0"
                  src="https://www.youtube.com/embed/HsLqiShzP0k?rel=0"
                  allowFullScreen
                ></iframe>
              </div>
            </Card>
          </div>
        </div>
      </Container>
    </>
  );
}

{
  /* <button
            className="btn btn-outline-danger mx-2 mb-3"
            style={{ borderRadius: "50px", fontWeight: "bold" }}
            onClick={startHandler}
          >
            Start Robot
          </button>


<button
  className="btn btn-outline-danger mx-2 mb-3"
  style={{ borderRadius: "50px", fontWeight: "bold" }}
  onClick={stopHandler}
>
  Stop Robot
</button>; */
}
export default App;
