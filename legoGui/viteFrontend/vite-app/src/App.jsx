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

  return (
    <>
      <nav class="navbar navbar-dark bg-primary mb-3">RuneStone GroupG</nav>

      <Container className="container-fluid mb-2 w-50 p-3">
        <div class="row">
          <div class="col-sm">
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
        <div class="row">
          <div class="col-sm">
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
                  Left
                </button>
                <div class="btn-group-vertical">
                  <button
                    type="button"
                    className="btn btn-primary btn-outline-danger my-3 btn-lg"
                    style={{
                      color: "white",
                    }}
                  >
                    Up
                  </button>
                  <button
                    type="button"
                    className="btn btn-primary btn-outline-danger my-3 btn-lg"
                    style={{
                      color: "white",
                    }}
                  >
                    Middle
                  </button>
                </div>
                <button
                  type="button"
                  className="btn btn-primary btn-outline-danger mx-1 btn-lg"
                  style={{
                    color: "white",
                  }}
                >
                  Right
                </button>
              </div>
            </Card>
          </div>

          {/* Rotate Section */}
          <div class="col-sm">
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
                <div class="btn-group-vertical">
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
          <div class="col-sm">
            <Card className="border border-primary">
              Youtube Live
              <div class="embed-responsive embed-responsive-1by1">
                <iframe
                  class="embed-responsive-item"
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
