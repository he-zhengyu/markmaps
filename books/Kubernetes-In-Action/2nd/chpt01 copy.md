---
markmap:
  initialExpandLevel: -1
  maxWidth: 0
  colorFreezeLevel: 3
---

# Introducing Kubernetes

## 1.1 Introducing Kubernetes
### 1.1.1 Kubernetes in a nutshell
- 🔑 **Kubernetes (K8s)** — software system for automating deployment & management of apps
- Name origin — Greek for *pilot / helmsman*; abbreviated **K8s** (8 letters between K and s)
- 💡 Lets you run software apps on thousands of nodes **as if all were one enormous computer**
- What it does for you
  - Abstracts away the underlying infrastructure
  - Simplifies development, deployment & management
- Who benefits
  - **Developers** — deploy without knowing hardware details
  - **Ops/SRE** — keep systems running with less manual effort

### 1.1.2 About the Kubernetes project
- Origin — developed by **Google**, drawing on years running **Borg** & **Omega**
- Open-sourced in **2014**; v1.0 in **2015**
- Handed to the **Cloud Native Computing Foundation (CNCF)**
- Written in **Go**
- 📌 Huge, active community; thousands of contributors
- Release cadence — AI-added: roughly **three minor releases per year**

### 1.1.3 Understanding why Kubernetes is so popular
- 💡 Three trends converged to drive adoption
- Shift to **microservices**
  - Monoliths split into many independently deployable components
  - ⚠️ Number of deployable parts explodes → manual ops impractical
- Move to **cloud-native / continuous delivery**
  - Faster, more frequent releases demanded
- Spread of **containers** (e.g. `Docker`)
  - Lightweight isolation; consistent across environments
- What K8s adds — automates running, connecting & scaling all these pieces

## 1.2 Understanding Kubernetes
### 1.2.1 How Kubernetes transforms a computer cluster
- Presents many machines as a **single deployment platform**
- 💡 Acts as an **operating system for the cluster**
  - Service discovery, scaling, load balancing, self-healing, scheduling
- Developers deploy **through Kubernetes**, not onto specific servers
- ⚠️ You stop thinking about *which* server — K8s decides placement

### 1.2.2 The benefits of using Kubernetes
- ✅ **Self-service deployment** — developers deploy on their own
- ✅ **Reducing the burden on ops teams** — automation handles routine failures
- ✅ **Better hardware utilization** — efficient bin-packing of workloads
- ✅ **Automated health checks & self-healing** — restarts/reschedules failed apps
- ✅ **Autoscaling** — adjusts to current load
- ✅ **Simplified deployment** — same workflow on any infrastructure

### 1.2.3 The architecture of a Kubernetes cluster
- A cluster = **Control Plane** + **Worker Nodes**
- **Control Plane** — controls & manages the whole cluster
  - 🔑 `API Server` — single entry point; you & components talk to it
  - 🔑 `etcd` — distributed datastore; persists all cluster state
  - 🔑 `Scheduler` — decides which worker node runs each application
  - 🔑 `Controller Manager` — control loops that reconcile cluster state
- **Worker Nodes** — run your containerized applications
  - 🔑 `Kubelet` — talks to API server, manages containers on its node
  - 🔑 `Kube Proxy` — load-balances traffic between application components
  - 🔑 **Container Runtime** — runs the containers (`containerd`, `CRI-O`, etc.)
- 💡 Control plane = the brain; worker nodes do the actual work

### 1.2.4 How Kubernetes runs an application
- Step 1 — package app components into **container images**
- Step 2 — push images to an **image registry**
- Step 3 — describe app in a **manifest** (YAML/JSON)
  - Declares **Deployments**, **Pods**, replica counts, images, etc.
- Step 4 — post the manifest to the **API Server**
- What happens next
  - State stored in `etcd`
  - **Scheduler** assigns groups of containers to worker nodes
  - **Kubelet** tells the runtime to pull images & run containers
- 🔑 **Pod** — group of one or more co-located containers; smallest deployable unit
- Keeping it running
  - Controllers continuously compare **desired vs actual** state
  - ⚠️ Dead containers/pods are **replaced**, nodes failover automatically
- 💡 Declarative model — you state the *what*, K8s figures out the *how*

## 1.3 Introducing Kubernetes into your organization
### 1.3.1 Running Kubernetes on-premises and in the cloud
- **On-premises** — run on your own infrastructure
- **Cloud** — use a hosted/managed offering
  - `GKE` (Google), `EKS` (AWS), `AKS` (Azure)
- ✅ Same workloads & API run anywhere → strong portability
- Hybrid setups also possible

### 1.3.2 To manage or not to manage Kubernetes yourself
- **Manage it yourself**
  - ✅ Full control & flexibility
  - ⚠️ Significant operational effort, expertise & maintenance
- **Use a managed service**
  - ✅ Provider runs the control plane, upgrades, availability
  - ⚠️ Less control; possible vendor lock-in

### 1.3.3 Using vanilla or extended Kubernetes
- **Vanilla** — pure upstream Kubernetes
- **Extended distributions**
  - e.g. **OpenShift**, **Rancher**
  - Add security, tooling & developer experience on top
- ⚠️ Extra features vs added complexity / lock-in

### 1.3.4 Should you even use Kubernetes?
- ✅ Worth it when
  - Many components / microservices to run
  - Need scaling, automation, resilience
  - Frequent deployments
- ❌ Possibly not worth it when
  - App has only a handful of components
  - Small team without ops capacity
  - Static, low-change workloads
- 💡 Kubernetes brings power **and** operational complexity — weigh both

## Key Takeaways
- 🔑 **Kubernetes** makes a cluster of machines behave like a single deployment platform
- 💡 You declare **desired state**; the control plane continuously reconciles actual to desired
- Architecture splits into **control plane** (API server, etcd, scheduler, controllers) and **worker nodes** (kubelet, kube proxy, runtime)
- 📌 The **Pod** is the smallest deployable unit — scheduled, monitored & self-healed automatically
- ✅ Runs the same way **on-premises and across clouds** — strong portability
- ⚠️ Adopt it only when microservices, scale, or frequent deployments justify the operational cost