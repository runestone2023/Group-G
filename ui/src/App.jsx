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
  const [idValue, setId] = useState("");
  let id = 0;

  function handle() {
    id = idValue;
    console.log(id);
  }

  const radioButtonClicked = (e) => {
    // setId(e.target.value);
    id = e.target.value;
    console.log(id);
  };

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

  const learnHandler = () => {
    axios
      .post(`http://localhost:8000/clients/${id}/learn`, {
        iters: 100,
      })
      .then((res) => console.log(res.data, res));
  };

  // move forward
  const moveForwardHandler = () => {
    axios
      .post(`http://localhost:8000/clients/${id}/move`, {
        speed: 100,
      })
      .then((res) => console.log(res.data, res));
  };

  // break
  const breakHandler = () => {
    axios
      .post(`http://localhost:8000/clients/${id}/move`, {
        speed: 0,
      })
      .then((res) => console.log(res.data, res));
  };

  // back
  const moveBackHandler = () => {
    axios
      .post(`http://localhost:8000/clients/${id}/move`, {
        speed: -100,
      })
      .then((res) => console.log(res.data, res));
  };

  const moveLeftHandler = () => {
    axios
      .post(`http://localhost:8000/clients/${id}/rotate`, {
        angle: -45,
      })
      .then((res) => console.log(res.data, res));
  };

  const moveRightHandler = () => {
    axios
      .post(`http://localhost:8000/clients/${id}/rotate`, {
        angle: 45,
      })
      .then((res) => console.log(res.data, res));
  };

  // claw on
  const clawOnHandler = () => {
    axios
      .post(`http://localhost:8000/clients/${id}/claw`, {
        grab: true,
      })
      .then((res) => console.log(res.data, res));
  };

  // claw off
  const clawOffHandler = () => {
    axios
      .post(`http://localhost:8000/clients/${id}/claw`, {
        grab: false,
      })
      .then((res) => console.log(res.data, res));
  };

  return (
    <>
      <nav className="navbar navbar-dark bg-primary mb-3">RuneStone GroupG</nav>

      <Container className="container-fluid mb-2 w-50 p-3">
        <div className="row">
          {/* Robot Selection Panel */}
          <div className="col-sm">
            <Card className="border border-primary">
              <form class="form-inline">
                <div class="form-group">
                  <label for="inputRobot" class="sr-only">
                    Enter the Bot ID
                  </label>
                  <input
                    type="text"
                    class="form-control"
                    id="inputRobot"
                    placeholder="Bot id"
                    value={idValue}
                    onChange={(e) => {
                      setId(e.target.value);
                    }}
                  />
                </div>
                <button
                  type="button"
                  class="btn btn-primary mt-2"
                  onClick={handle}
                >
                  Confirm
                </button>
              </form>
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
                {/* Learn */}
                <button
                  type="button"
                  className="btn btn-primary btn-outline-danger mx-1 btn-lg"
                  style={{
                    color: "white",
                  }}
                  onClick={learnHandler}
                >
                  Learn
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
                  {/* Forward */}
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
                  {/* Break */}
                  <button
                    type="button"
                    className="btn btn-primary btn-outline-danger my-3 btn-lg"
                    style={{
                      color: "white",
                    }}
                    onClick={breakHandler}
                  >
                    Break
                  </button>
                  {/* back */}
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
              Claws
              <div
                className="btn-group"
                role="group"
                aria-label="Basic example"
              >
                <div className="btn-group-vertical">
                  <button
                    type="button"
                    className="btn btn-primary btn-outline-danger my-3 btn-lg"
                    style={{
                      color: "white",
                    }}
                    onClick={clawOnHandler}
                  >
                    Open
                  </button>
                  <button
                    type="button"
                    className="btn btn-primary btn-outline-danger my-3 btn-lg"
                    style={{
                      color: "white",
                    }}
                    onClick={clawOffHandler}
                  >
                    Close
                  </button>
                </div>
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
