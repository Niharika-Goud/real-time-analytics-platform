import React, { useEffect, useState } from "react";
import axios from "axios";

import {
  BarChart,
  Bar,
  PieChart,
  Pie,
  LineChart,
  Line,
  XAxis,
  YAxis,
  Tooltip,
  CartesianGrid,
  Legend
} from "recharts";

function Dashboard() {

  // Analytics statistics state
  const [stats, setStats] = useState({
    total_events: 0,
    unique_users: 0,
    top_event: ""
  });

  // Live event stream state
  const [liveEvents, setLiveEvents] = useState([]);

  // Alert notifications state
  const [alerts, setAlerts] = useState([]);

  // Fetch analytics statistics from backend
  const fetchStats = async () => {

    try {

      const response = await axios.get(
        "http://127.0.0.1:8000/analytics/stats",
        {
          headers: {
            Authorization:
              `Bearer ${localStorage.getItem("token")}`
          }
        }
      );

      setStats(response.data);

    } catch (error) {

      console.error(error);
    }
  };

  // WebSocket connection for real-time updates
  useEffect(() => {

    fetchStats();

    const ws = new WebSocket(
  "ws://127.0.0.1:8000/ws/events"
);

ws.onopen = () => {

  console.log("WebSocket Connected");

  // Send heartbeat message
  ws.send("connected");
};

    // Handle incoming websocket messages
    ws.onmessage = (event) => {

      const data = JSON.parse(event.data);

      console.log("Live Message:", data);

      // Handle alert notifications
      if (data.type === "alert") {

        setAlerts((prev) => [
          data.message,
          ...prev
        ]);

        return;
      }

      // Handle live event updates
      setLiveEvents((prev) => [
        {
          event_type: data.event_type,
          user: data.user
        },
        ...prev
      ]);

      fetchStats();
    };

    // Cleanup websocket on component unmount
    return () => ws.close();

  }, []);

  // Chart data
  const chartData = [
    {
      name: "Events",
      value: stats.total_events
    },
    {
      name: "Users",
      value: stats.unique_users
    }
  ];

  return (

    <div
      style={{
        padding: "40px",
        fontFamily: "Arial",
        minHeight: "100vh",
        background:
          "linear-gradient(135deg, #0f172a, #111827, #1e3a8a)"
      }}
    >

      {/* Dashboard Title */}

      <h1
        style={{
          color: "#f8fafc",
          marginBottom: "10px",
          fontSize: "48px",
          fontWeight: "700"
        }}
      >
        Real-Time Analytics Dashboard
      </h1>

      {/* Dashboard Subtitle */}

      <p
        style={{
          color: "#cbd5e1",
          marginBottom: "20px",
          fontSize: "18px"
        }}
      >
        Monitor live platform activity,
        user engagement, and analytics
        in real time 🚀
      </p>

      {/* Decorative Gradient Line */}

      <div
        style={{
          height: "4px",
          width: "140px",
          background:
            "linear-gradient(to right, #38bdf8, #8b5cf6)",
          borderRadius: "20px",
          marginBottom: "50px"
        }}
      ></div>

      {/* Analytics Summary Cards */}

      <div
        style={{
          display: "flex",
          gap: "30px",
          flexWrap: "wrap",
          marginBottom: "60px"
        }}
      >

        {/* Total Events Card */}

        <div
          style={{
            ...cardStyle,
            background:
              "linear-gradient(135deg, #2563eb, #38bdf8)"
          }}
        >

          <h2>Total Events</h2>

          <p
            style={{
              fontSize: "48px",
              fontWeight: "bold",
              marginTop: "20px"
            }}
          >
            {stats.total_events}
          </p>

        </div>

        {/* Unique Users Card */}

        <div
          style={{
            ...cardStyle,
            background:
              "linear-gradient(135deg, #059669, #34d399)"
          }}
        >

          <h2>Unique Users</h2>

          <p
            style={{
              fontSize: "48px",
              fontWeight: "bold",
              marginTop: "20px"
            }}
          >
            {stats.unique_users}
          </p>

        </div>

        {/* Top Event Card */}

        <div
          style={{
            ...cardStyle,
            background:
              "linear-gradient(135deg, #7c3aed, #c084fc)"
          }}
        >

          <h2>Top Event</h2>

          <p
            style={{
              fontSize: "32px",
              fontWeight: "bold",
              marginTop: "25px"
            }}
          >
            {stats.top_event}
          </p>

        </div>

      </div>

      {/* Alerts Section */}

      <div
        style={{
          marginBottom: "40px"
        }}
      >

        <h2
          style={{
            color: "#facc15",
            marginBottom: "20px"
          }}
        >
          🚨 Alerts
        </h2>

        {

          alerts.map((alert, index) => (

            <div
              key={index}
              style={{
                backgroundColor: "#7f1d1d",
                color: "white",
                padding: "15px",
                borderRadius: "12px",
                marginBottom: "12px",
                boxShadow:
                  "0 0 15px rgba(255,0,0,0.3)"
              }}
            >
              {alert}
            </div>
          ))
        }

      </div>

      {/* Charts Section */}

      <div
        style={{
          display: "flex",
          flexWrap: "wrap",
          gap: "40px",
          justifyContent: "center",
          marginBottom: "70px"
        }}
      >

        {/* Bar Chart */}

        <div style={chartContainerStyle}>

          <BarChart
            width={500}
            height={320}
            data={chartData}
          >

            <CartesianGrid strokeDasharray="3 3" />

            <XAxis
              dataKey="name"
              stroke="#cbd5e1"
            />

            <YAxis stroke="#cbd5e1" />

            <Tooltip />

            <Bar
              dataKey="value"
              fill="#38bdf8"
              radius={[12, 12, 0, 0]}
            />

          </BarChart>

        </div>

        {/* Pie Chart */}

        <div style={chartContainerStyle}>

          <PieChart width={400} height={320}>

            <Pie
              data={chartData}
              dataKey="value"
              nameKey="name"
              outerRadius={100}
              fill="#8884d8"
              label
            />

            <Tooltip />

            <Legend />

          </PieChart>

        </div>

        {/* Line Chart */}

        <div style={chartContainerStyle}>

          <LineChart
            width={500}
            height={320}
            data={chartData}
          >

            <XAxis
              dataKey="name"
              stroke="#cbd5e1"
            />

            <YAxis stroke="#cbd5e1" />

            <Tooltip />

            <Line
              type="monotone"
              dataKey="value"
              stroke="#82ca9d"
              strokeWidth={3}
            />

          </LineChart>

        </div>

      </div>

      {/* Live Events Section */}

      <div>

        <h2
          style={{
            color: "#f8fafc",
            marginBottom: "25px",
            fontSize: "32px"
          }}
        >
          🔴 Live Events
        </h2>

        {

          liveEvents.map((event, index) => (

            <div
              key={index}
              style={eventStyle}
            >

              <p
                style={{
                  fontSize: "18px"
                }}
              >
                <strong>Event:</strong>
                {" "}
                {event.event_type}
              </p>

              <p
                style={{
                  fontSize: "18px"
                }}
              >
                <strong>User:</strong>
                {" "}
                {event.user}
              </p>

            </div>
          ))
        }

      </div>

    </div>
  );
}


// Shared analytics card style
const cardStyle = {

  padding: "28px",
  borderRadius: "24px",
  width: "260px",
  color: "white",
  cursor: "pointer",
  transition: "all 0.3s ease",
  boxShadow:
    "0 0 25px rgba(59,130,246,0.25)"
};


// Shared chart container style
const chartContainerStyle = {

  backgroundColor: "#0b1120",
  padding: "25px",
  borderRadius: "25px",
  boxShadow:
    "0 0 35px rgba(59,130,246,0.18)"
};


// Live event card style
const eventStyle = {

  padding: "20px",
  borderRadius: "16px",
  backgroundColor: "#111827",
  color: "white",
  marginBottom: "18px",
  boxShadow:
    "0 0 18px rgba(59,130,246,0.18)",
  borderLeft: "5px solid #38bdf8"
};


export default Dashboard;