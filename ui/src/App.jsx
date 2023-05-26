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
  const [bots, setBots] = useState([]);

  let id = 0;
  let speed = 50;
  let positiveAngle = 45;
  let negativeAngle = -45;

  function selectBot(botId) {
    id = botId;
    console.log(id);
    // alert("Bot Changed");
  }

  function selectBotSpeed(botSpeed) {
    speed = botSpeed;
    console.log(speed);
    // alert("Bot Changed");
  }

  function selectClawAngle(clawAngle) {
    positiveAngle = clawAngle;
    negativeAngle = -clawAngle;
    console.log(positiveAngle, negativeAngle);
    // alert("Bot Changed");
  }

  const getHandle = () => {
    axios
      .get(`http://localhost:8000/clients`)
      // .then(() => console.log(res.data))
      .then((res) => setBots(res.data));
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
        speed: speed,
      })
      .then((res) => console.log(res.data));
    console.log("this is sppe", speed);
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
        speed: -speed,
      })
      .then((res) => console.log(res.data, res));
  };

  const moveLeftHandler = () => {
    axios
      .post(`http://localhost:8000/clients/${id}/rotate`, {
        angle: negativeAngle,
      })
      .then((res) => console.log(res.data, res));
  };

  const moveRightHandler = () => {
    axios
      .post(`http://localhost:8000/clients/${id}/rotate`, {
        angle: positiveAngle,
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
    <Container data-bs-theme="light">
      <nav
        className="navbar navbar-dark bg-warning text-dark rounded-bottom"
        style={{ justifyContent: "center" }}
      >
        <a class="navbar-brand">
          <img src="src/assets/uu.png" width="30" height="30" alt="" />
        </a>
        RuneStone GroupG
        <a class="navbar-brand mx-3">
          <img src="src/assets/han.png" width="30" height="30" alt="" />
        </a>
      </nav>

      <Container className="container container-sm mb-2 w-50 p-3">
        <div className="row">
          {/* Robot Selection Panel */}
          <div className="col-sm h-25 d-flex justify-content-start">
            <Card className="border border-warning bg-dark text-white">
              <form className="form-inline">
                <div className="form-group">
                  <label for="inputRobot" className="sr-only">
                    Select Bot
                  </label>
                </div>

                <button
                  type="button"
                  className="btn btn-warning text-dark btn-outline-danger  m-1"
                  onClick={getHandle}
                >
                  SCAN
                </button>
              </form>
              {bots.length > 0 && (
                <div
                  className="btn-group btn-group-toggle"
                  data-toggle="buttons"
                >
                  <ul className="mx-auto justify-content-center">
                    {bots.map((bot) => (
                      <label className="btn btn-outline-secondary btn-sm m-1 active">
                        <input
                          type="radio"
                          // className="btn btn-sm m-1"
                          name="options"
                          // data-toggle="button"
                          // aria-pressed="false"
                          id={bot}
                          key={bot}
                          autoComplete="off"
                          value={bot}
                          onClick={(e) => {
                            selectBot(e.target.value);
                            // selectBot();
                          }}
                          // checked
                          // onClick={selectBot}
                        />
                        {bot}
                      </label>
                    ))}
                  </ul>
                </div>
              )}
            </Card>
          </div>

          {/* Power Mode */}
          <div className="col-sm h-25 d-flex justify-content-start">
            <Card className="border border-warning bg-dark text-white">
              Mode
              <div
                className="btn-group btn-group-sm btn-group-vertical"
                role="group"
                aria-label="Basic example"
              >
                <button
                  type="button"
                  className="btn btn-warning text-dark btn-outline-danger mx-1 btn-lg"
                  style={{
                    color: "white",
                  }}
                  onClick={startHandler}
                >
                  Manuel
                </button>
                <button
                  type="button"
                  className="btn btn-warning text-dark btn-outline-danger mx-1 btn-lg"
                  style={{
                    color: "white",
                  }}
                  onClick={stopHandler}
                >
                  Automatic
                </button>
                {/* Learn */}
                <button
                  type="button"
                  className="btn btn-warning text-dark btn-outline-danger mx-1 btn-lg"
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
            <Card className="border border-warning bg-dark text-white">
              Controls
              <div
                className="btn-group"
                role="group"
                aria-label="Basic example"
              >
                <button
                  type="button"
                  className="btn btn-warning text-dark btn-outline-danger mx-1 btn-lg"
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
                    className="btn btn-warning text-dark btn-outline-danger my-3 btn-lg"
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
                    className="btn btn-warning text-dark btn-outline-danger my-3 btn-lg"
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
                    className="btn btn-warning text-dark btn-outline-danger my-3 btn-lg"
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
                  className="btn btn-warning text-dark btn-outline-danger mx-1 btn-lg"
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

          <div className="col-sm">
            <Card className="border border-warning bg-dark text-white">
              Speed
              <div
                className="btn-group-vertical btn-group-toggle btn-group-sm"
                data-toggle="buttons"
              >
                <label className="btn btn-outline-secondary active bg-dark">
                  <input
                    type="radio"
                    name="Speed"
                    id="speedOptions1"
                    autoComplete="off"
                    value={"10"}
                    onClick={(e) => {
                      selectBotSpeed(e.target.value);
                    }}
                  />
                  SLOW
                </label>
                <label className="btn btn-secondary bg-dark">
                  <input
                    type="radio"
                    name="Speed"
                    id="speedOptions2"
                    autoComplete="off"
                    value={"50"}
                    onClick={(e) => {
                      selectBotSpeed(e.target.value);
                    }}
                  />
                  MEDIUM
                </label>
                <label className="btn btn-secondary bg-dark">
                  <input
                    type="radio"
                    name="Speed"
                    id="speedOptions3"
                    autoComplete="off"
                    value={"100"}
                    onClick={(e) => {
                      selectBotSpeed(e.target.value);
                    }}
                  />
                  FAST
                </label>
              </div>
              Angle
              <div class="col-xs-2">
                <input
                  class="form-control"
                  id="angle"
                  type="number"
                  style={{
                    backgroundColor: "#212529",
                    color: "white",
                  }}
                  min={1}
                  onChange={(e) => {
                    selectClawAngle(e.target.value);
                  }}
                />
              </div>
            </Card>
          </div>

          {/* Claw Section */}
          <div className="col-sm">
            <Card className="border border-warning bg-dark text-white">
              Claws
              {/* <div
                className="btn-group"
                role="group"
                aria-label="Basic example"
              >
                <div className="btn-group-vertical">
                  <button
                    type="button"
                    className="btn btn-warning text-dark btn-outline-danger my-3 btn-lg"
                    style={{
                      color: "white",
                    }}
                    onClick={clawOnHandler}
                  >
                    Open
                  </button>
                  <button
                    type="button"
                    className="btn btn-warning text-dark btn-outline-danger my-3 btn-lg"
                    style={{
                      color: "white",
                    }}
                    onClick={clawOffHandler}
                  >
                    Close
                  </button>
                </div>
              </div> */}
              <button
                className="btn btn-warning btn-outline-danger text-dark m-2"
                onClick={clawOnHandler}
              >
                Up
              </button>
              <button
                className="btn btn-warning btn-outline-danger text-dark m-2"
                onClick={clawOffHandler}
              >
                Down
              </button>
            </Card>
          </div>
          {/* Liive Stream */}
          {/* <div className="col-sm">
            <Card className="border border-warning bg-dark text-white">
              Youtube Live
              <div className="embed-responsive embed-responsive-1by1">
                <iframe
                  className="embed-responsive-item"
                  // src="https://www.youtube.com/embed/zpOULjyy-n8?rel=0"
                  // src="https://www.youtube.com/embed/HsLqiShzP0k?rel=0"
                  src="https://youtube.com/live/bosNdn6iJAI?feature=share"
                  allowFullScreen
                ></iframe>
              </div>
            </Card>
          </div> */}
        </div>
      </Container>
    </Container>
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
