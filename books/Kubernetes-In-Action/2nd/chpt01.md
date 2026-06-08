---
markmap:
  initialExpandLevel: -1
  maxWidth: 0
  colorFreezeLevel: 3
---

# Introducing Kubernetes

## 1.1 Introducing Kubernetes
### 1.1.1 Kubernetes in a nutshell
- 🔑 **Kubernetes (K8s)** — open-source system for automating deployment, scaling & management of containerized apps
- Name origin — Greek for *helmsman/pilot*
- 💡 Abstracts the underlying infrastructure
  - Treats all nodes as a **single pool of resources**
  - Developers deploy without knowing which server runs the app
- Core function
  - You describe **desired state**; K8s makes reality match it
  - Self-healing, automated scheduling

### 1.1.2 About the Kubernetes project
- Origin — born at **Google**, inspired by internal systems **Borg** & **Omega**
- Open-sourced in **2014**
- Donated to the **Cloud Native Computing Foundation (CNCF)**
- Written in **Go**
- 📌 One of the most widely-adopted open-source projects
- AI-added: Release naming — version 1.0 reached in **2015**

### 1.1.3 Understanding why Kubernetes is so popular
- Rise of **microservices**
  - Apps split into many small, independent components
  - ⚠️ Manual management becomes unmanageable at scale
- Spread of **containers** (e.g. `Docker`)
  - Lightweight, portable, consistent environments
- Demand for automation
  - ✅ Consistent deploys across dev, test, prod
- Decoupling dev from ops
  - Developers focus on app logic
  - Ops focus on infrastructure

## 1.2 Understanding Kubernetes
### 1.2.1 How Kubernetes transforms a computer cluster
- Turns many machines into **one logical computer**
- 💡 Acts like an **operating system for the cluster**
  - Schedules workloads onto nodes
  - Handles service discovery, scaling, failover
- Developers submit apps via the **API**, not to specific machines

### 1.2.2 The benefits of using Kubernetes
- ✅ **Self-service deployment** for developers
- ✅ **Better hardware utilization** — efficient bin-packing of workloads
- ✅ **Automated health management**
  - Restarts failed containers
  - Reschedules off dead nodes
- ✅ **Autoscaling** to match load
- ✅ **Simplified app deployment** regardless of infrastructure
- 📊 Higher infrastructure efficiency & reduced ops cost

### 1.2.3 The architecture of a Kubernetes cluster
- Two node types
  - **Control Plane** (master) — controls & manages the cluster
    - 🔑 `API Server` — front-end, all communication passes through it
    - 🔑 `etcd` — distributed key-value store, holds cluster state
    - 🔑 `Scheduler` — assigns Pods to worker nodes
    - 🔑 `Controller Manager` — runs control loops, reconciles state
  - **Worker Nodes** — run the actual application workloads
    - 🔑 `Kubelet` — agent managing containers on the node
    - 🔑 `Kube-proxy` — load-balances network traffic between components
    - 🔑 **Container Runtime** — runs containers (e.g. `containerd`, `CRI-O`)
- 💡 Control plane = the brain; worker nodes = the muscle

### 1.2.4 How Kubernetes runs an application
- Package app into **container images**
- Describe app in a **manifest** (YAML/JSON)
  - Defines **Pods**, **Deployments**, replica count, images
- Submit manifest to the **API Server**
- Control plane workflow
  - Stored in `etcd`
  - **Scheduler** picks suitable nodes
  - **Kubelet** instructs runtime to pull images & run containers
- 🔑 **Pod** — smallest deployable unit; one or more containers
- Keeping it running
  - Controllers continuously reconcile **desired vs actual** state
  - ⚠️ Failed pods are recreated, not repaired

## 1.3 Introducing Kubernetes into your organization
### 1.3.1 Running Kubernetes on-premises and in the cloud
- **On-premises** — full control, your own hardware
- **Cloud** — managed offerings
  - `GKE` (Google), `EKS` (AWS), `AKS` (Azure)
- ✅ Same API & workloads run anywhere → portability

### 1.3.2 To manage or not to manage Kubernetes yourself
- **Self-managed**
  - ✅ Maximum control & customization
  - ⚠️ High operational complexity & maintenance burden
- **Managed service**
  - ✅ Provider handles control plane, upgrades, availability
  - ⚠️ Less control, potential vendor lock-in

### 1.3.3 Using vanilla or extended Kubernetes
- **Vanilla** — pure upstream Kubernetes
- **Extended distributions**
  - e.g. **OpenShift**, **Rancher**
  - Add tooling, security, developer experience
- ⚠️ Trade-off: extra features vs added complexity / lock-in

### 1.3.4 Should you even use Kubernetes?
- ✅ Good fit
  - Many microservices / containers
  - Need for scaling, automation, resilience
- ❌ Possibly overkill
  - Small apps, few components
  - Limited team / ops expertise
- 💡 Kubernetes adds power **and** operational complexity — weigh both

## Key Takeaways
- 🔑 **Kubernetes** abstracts a cluster of machines into a single deployment platform
- 💡 You declare **desired state**; the control plane continuously reconciles reality to match
- Architecture splits into **control plane** (brain) and **worker nodes** (muscle)
- 📌 The **Pod** is the smallest deployable unit, scheduled and self-healed automatically
- ✅ Runs identically **on-premises and across clouds** — strong portability
- ⚠️ Powerful but complex — adopt only when microservices/scale justify the operational cost