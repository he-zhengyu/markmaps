# Kubernetes in Action *(p. 1)*
# brief contents *(p. 9)*
# contents *(p. 11)*
# preface *(p. 23)*
# acknowledgments *(p. 25)*
# about this book *(p. 27)*
## Who should read this book *(p. 27)*
## How this book is organized: a roadmap *(p. 28)*
## About the code *(p. 29)*
## Book forum *(p. 30)*
## Other online resources *(p. 30)*
# about the author *(p. 31)*
# about the cover illustration *(p. 32)*
# Part 1 Overview *(p. 33)*
## 1 Introducing Kubernetes *(p. 33)*
### 1.1 Understanding the need for a system like Kubernetes *(p. 34)*
#### 1.1.1 Moving from monolithic apps to microservices *(p. 35)*
#### 1.1.2 Providing a consistent environment to applications *(p. 38)*
#### 1.1.3 Moving to continuous delivery: DevOps and NoOps *(p. 38)*
### 1.2 Introducing container technologies *(p. 39)*
#### 1.2.1 Understanding what containers are *(p. 40)*
#### 1.2.2 Introducing the Docker container platform *(p. 44)*
#### 1.2.3 Introducing rkt—an alternative to Docker *(p. 47)*
### 1.3 Introducing Kubernetes *(p. 48)*
#### 1.3.1 Understanding its origins *(p. 48)*
#### 1.3.2 Looking at Kubernetes from the top of a mountain *(p. 48)*
#### 1.3.3 Understanding the architecture of a Kubernetes cluster *(p. 50)*
#### 1.3.4 Running an application in Kubernetes *(p. 51)*
#### 1.3.5 Understanding the benefits of using Kubernetes *(p. 53)*
### 1.4 Summary *(p. 55)*
## 2 First steps with Docker and Kubernetes *(p. 57)*
### 2.1 Creating, running, and sharing a container image *(p. 58)*
#### 2.1.1 Installing Docker and running a Hello World container *(p. 58)*
#### 2.1.2 Creating a trivial Node.js app *(p. 60)*
#### 2.1.3 Creating a Dockerfile for the image *(p. 61)*
#### 2.1.4 Building the container image *(p. 61)*
#### 2.1.5 Running the container image *(p. 64)*
#### 2.1.6 Exploring the inside of a running container *(p. 65)*
#### 2.1.7 Stopping and removing a container *(p. 66)*
#### 2.1.8 Pushing the image to an image registry *(p. 67)*
### 2.2 Setting up a Kubernetes cluster *(p. 68)*
#### 2.2.1 Running a local single-node Kubernetes cluster with Minikube *(p. 69)*
#### 2.2.2 Using a hosted Kubernetes cluster with Google Kubernetes Engine *(p. 70)*
#### 2.2.3 Setting up an alias and command-line completion for kubectl *(p. 73)*
### 2.3 Running your first app on Kubernetes *(p. 74)*
#### 2.3.1 Deploying your Node.js app *(p. 74)*
#### 2.3.2 Accessing your web application *(p. 77)*
#### 2.3.3 The logical parts of your system *(p. 79)*
#### 2.3.4 Horizontally scaling the application *(p. 80)*
#### 2.3.5 Examining what nodes your app is running on *(p. 83)*
#### 2.3.6 Introducing the Kubernetes dashboard *(p. 84)*
### 2.4 Summary *(p. 85)*
# Part 2 Core concepts *(p. 87)*
## 3 Pods: running containers in Kubernetes *(p. 87)*
### 3.1 Introducing pods *(p. 88)*
#### 3.1.1 Understanding why we need pods *(p. 88)*
#### 3.1.2 Understanding pods *(p. 89)*
#### 3.1.3 Organizing containers across pods properly *(p. 90)*
### 3.2 Creating pods from YAML or JSON descriptors *(p. 93)*
#### 3.2.1 Examining a YAML descriptor of an existing pod *(p. 93)*
#### 3.2.2 Creating a simple YAML descriptor for a pod *(p. 95)*
#### 3.2.3 Using kubectl create to create the pod *(p. 97)*
#### 3.2.4 Viewing application logs *(p. 97)*
#### 3.2.5 Sending requests to the pod *(p. 98)*
### 3.3 Organizing pods with labels *(p. 99)*
#### 3.3.1 Introducing labels *(p. 100)*
#### 3.3.2 Specifying labels when creating a pod *(p. 101)*
#### 3.3.3 Modifying labels of existing pods *(p. 102)*
### 3.4 Listing subsets of pods through label selectors *(p. 103)*
#### 3.4.1 Listing pods using a label selector *(p. 103)*
#### 3.4.2 Using multiple conditions in a label selector *(p. 104)*
### 3.5 Using labels and selectors to constrain pod scheduling *(p. 105)*
#### 3.5.1 Using labels for categorizing worker nodes *(p. 106)*
#### 3.5.2 Scheduling pods to specific nodes *(p. 106)*
#### 3.5.3 Scheduling to one specific node *(p. 107)*
### 3.6 Annotating pods *(p. 107)*
#### 3.6.1 Looking up an object’s annotations *(p. 107)*
#### 3.6.2 Adding and modifying annotations *(p. 108)*
### 3.7 Using namespaces to group resources *(p. 108)*
#### 3.7.1 Understanding the need for namespaces *(p. 109)*
#### 3.7.2 Discovering other namespaces and their pods *(p. 109)*
#### 3.7.3 Creating a namespace *(p. 110)*
#### 3.7.4 Managing objects in other namespaces *(p. 111)*
#### 3.7.5 Understanding the isolation provided by namespaces *(p. 111)*
### 3.8 Stopping and removing pods *(p. 112)*
#### 3.8.1 Deleting a pod by name *(p. 112)*
#### 3.8.2 Deleting pods using label selectors *(p. 112)*
#### 3.8.3 Deleting pods by deleting the whole namespace *(p. 112)*
#### 3.8.4 Deleting all pods in a namespace, while keeping the namespace *(p. 113)*
#### 3.8.5 Deleting (almost) all resources in a namespace *(p. 114)*
### 3.9 Summary *(p. 114)*
## 4 Replication and other controllers: deploying managed pods *(p. 116)*
### 4.1 Keeping pods healthy *(p. 117)*
#### 4.1.1 Introducing liveness probes *(p. 117)*
#### 4.1.2 Creating an HTTP-based liveness probe *(p. 118)*
#### 4.1.3 Seeing a liveness probe in action *(p. 119)*
#### 4.1.4 Configuring additional properties of the liveness probe *(p. 120)*
#### 4.1.5 Creating effective liveness probes *(p. 121)*
### 4.2 Introducing ReplicationControllers *(p. 122)*
#### 4.2.1 The operation of a ReplicationController *(p. 123)*
#### 4.2.2 Creating a ReplicationController *(p. 125)*
#### 4.2.3 Seeing the ReplicationController in action *(p. 126)*
#### 4.2.4 Moving pods in and out of the scope of a ReplicationController *(p. 130)*
#### 4.2.5 Changing the pod template *(p. 133)*
#### 4.2.6 Horizontally scaling pods *(p. 134)*
#### 4.2.7 Deleting a ReplicationController *(p. 135)*
### 4.3 Using ReplicaSets instead of ReplicationControllers *(p. 136)*
#### 4.3.1 Comparing a ReplicaSet to a ReplicationController *(p. 137)*
#### 4.3.2 Defining a ReplicaSet *(p. 137)*
#### 4.3.3 Creating and examining a ReplicaSet *(p. 138)*
#### 4.3.4 Using the ReplicaSet’s more expressive label selectors *(p. 139)*
#### 4.3.5 Wrapping up ReplicaSets *(p. 140)*
### 4.4 Running exactly one pod on each node with DaemonSets *(p. 140)*
#### 4.4.1 Using a DaemonSet to run a pod on every node *(p. 141)*
#### 4.4.2 Using a DaemonSet to run pods only on certain nodes *(p. 141)*
### 4.5 Running pods that perform a single completable task *(p. 144)*
#### 4.5.1 Introducing the Job resource *(p. 144)*
#### 4.5.2 Defining a Job resource *(p. 145)*
#### 4.5.3 Seeing a Job run a pod *(p. 146)*
#### 4.5.4 Running multiple pod instances in a Job *(p. 146)*
#### 4.5.5 Limiting the time allowed for a Job pod to complete *(p. 148)*
### 4.6 Scheduling Jobs to run periodically or once in the future *(p. 148)*
#### 4.6.1 Creating a CronJob *(p. 148)*
#### 4.6.2 Understanding how scheduled jobs are run *(p. 149)*
### 4.7 Summary *(p. 150)*
## 5 Services: enabling clients to discover and talk to pods *(p. 152)*
### 5.1 Introducing services *(p. 153)*
#### 5.1.1 Creating services *(p. 154)*
#### 5.1.2 Discovering services *(p. 160)*
### 5.2 Connecting to services living outside the cluster *(p. 163)*
#### 5.2.1 Introducing service endpoints *(p. 163)*
#### 5.2.2 Manually configuring service endpoints *(p. 164)*
#### 5.2.3 Creating an alias for an external service *(p. 166)*
### 5.3 Exposing services to external clients *(p. 166)*
#### 5.3.1 Using a NodePort service *(p. 167)*
#### 5.3.2 Exposing a service through an external load balancer *(p. 170)*
#### 5.3.3 Understanding the peculiarities of external connections *(p. 173)*
### 5.4 Exposing services externally through an Ingress resource *(p. 174)*
#### 5.4.1 Creating an Ingress resource *(p. 176)*
#### 5.4.2 Accessing the service through the Ingress *(p. 177)*
#### 5.4.3 Exposing multiple services through the same Ingress *(p. 178)*
#### 5.4.4 Configuring Ingress to handle TLS traffic *(p. 179)*
### 5.5 Signaling when a pod is ready to accept connections *(p. 181)*
#### 5.5.1 Introducing readiness probes *(p. 181)*
#### 5.5.2 Adding a readiness probe to a pod *(p. 183)*
#### 5.5.3 Understanding what real-world readiness probes should do *(p. 185)*
### 5.6 Using a headless service for discovering individual pods *(p. 186)*
#### 5.6.1 Creating a headless service *(p. 186)*
#### 5.6.2 Discovering pods through DNS *(p. 187)*
#### 5.6.3 Discovering all pods—even those that aren’t ready *(p. 188)*
### 5.7 Troubleshooting services *(p. 188)*
### 5.8 Summary *(p. 189)*
## 6 Volumes: attaching disk storage to containers *(p. 191)*
### 6.1 Introducing volumes *(p. 192)*
#### 6.1.1 Explaining volumes in an example *(p. 192)*
#### 6.1.2 Introducing available volume types *(p. 194)*
### 6.2 Using volumes to share data between containers *(p. 195)*
#### 6.2.1 Using an emptyDir volume *(p. 195)*
#### 6.2.2 Using a Git repository as the starting point for a volume *(p. 198)*
### 6.3 Accessing files on the worker node’s filesystem *(p. 201)*
#### 6.3.1 Introducing the hostPath volume *(p. 201)*
#### 6.3.2 Examining system pods that use hostPath volumes *(p. 202)*
### 6.4 Using persistent storage *(p. 203)*
#### 6.4.1 Using a GCE Persistent Disk in a pod volume *(p. 203)*
#### 6.4.2 Using other types of volumes with underlying persistent storage *(p. 206)*
### 6.5 Decoupling pods from the underlying storage technology *(p. 208)*
#### 6.5.1 Introducing PersistentVolumes and PersistentVolumeClaims *(p. 208)*
#### 6.5.2 Creating a PersistentVolume *(p. 209)*
#### 6.5.3 Claiming a PersistentVolume by creating a PersistentVolumeClaim *(p. 211)*
#### 6.5.4 Using a PersistentVolumeClaim in a pod *(p. 213)*
#### 6.5.5 Understanding the benefits of using PersistentVolumes and claims *(p. 214)*
#### 6.5.6 Recycling PersistentVolumes *(p. 215)*
### 6.6 Dynamic provisioning of PersistentVolumes *(p. 216)*
#### 6.6.1 Defining the available storage types through StorageClass resources *(p. 217)*
#### 6.6.2 Requesting the storage class in a PersistentVolumeClaim *(p. 217)*
#### 6.6.3 Dynamic provisioning without specifying a storage class *(p. 219)*
### 6.7 Summary *(p. 222)*
## 7 ConfigMaps and Secrets: configuring applications *(p. 223)*
### 7.1 Configuring containerized applications *(p. 223)*
### 7.2 Passing command-line arguments to containers *(p. 224)*
#### 7.2.1 Defining the command and arguments in Docker *(p. 225)*
#### 7.2.2 Overriding the command and arguments in Kubernetes *(p. 227)*
### 7.3 Setting environment variables for a container *(p. 228)*
#### 7.3.1 Specifying environment variables in a container definition *(p. 229)*
#### 7.3.2 Referring to other environment variables in a variable’s value *(p. 230)*
#### 7.3.3 Understanding the drawback of hardcoding environment variables *(p. 230)*
### 7.4 Decoupling configuration with a ConfigMap *(p. 230)*
#### 7.4.1 Introducing ConfigMaps *(p. 230)*
#### 7.4.2 Creating a ConfigMap *(p. 232)*
#### 7.4.3 Passing a ConfigMap entry to a container as an environment variable *(p. 234)*
#### 7.4.4 Passing all entries of a ConfigMap as environment variables at once *(p. 236)*
#### 7.4.5 Passing a ConfigMap entry as a command-line argument *(p. 236)*
#### 7.4.6 Using a configMap volume to expose ConfigMap entries as files *(p. 237)*
#### 7.4.7 Updating an app’s config without having to restart the app *(p. 243)*
### 7.5 Using Secrets to pass sensitive data to containers *(p. 245)*
#### 7.5.1 Introducing Secrets *(p. 246)*
#### 7.5.2 Introducing the default token Secret *(p. 246)*
#### 7.5.3 Creating a Secret *(p. 248)*
#### 7.5.4 Comparing ConfigMaps and Secrets *(p. 249)*
#### 7.5.5 Using the Secret in a pod *(p. 250)*
#### 7.5.6 Understanding image pull Secrets *(p. 254)*
### 7.6 Summary *(p. 256)*
## 8 Accessing pod metadata and other resources from applications *(p. 257)*
### 8.1 Passing metadata through the Downward API *(p. 258)*
#### 8.1.1 Understanding the available metadata *(p. 258)*
#### 8.1.2 Exposing metadata through environment variables *(p. 259)*
#### 8.1.3 Passing metadata through files in a downwardAPI volume *(p. 262)*
### 8.2 Talking to the Kubernetes API server *(p. 265)*
#### 8.2.1 Exploring the Kubernetes REST API *(p. 266)*
#### 8.2.2 Talking to the API server from within a pod *(p. 270)*
#### 8.2.3 Simplifying API server communication with ambassador containers *(p. 275)*
#### 8.2.4 Using client libraries to talk to the API server *(p. 278)*
### 8.3 Summary *(p. 281)*
## 9 Deployments: updating applications declaratively *(p. 282)*
### 9.1 Updating applications running in pods *(p. 283)*
#### 9.1.1 Deleting old pods and replacing them with new ones *(p. 284)*
#### 9.1.2 Spinning up new pods and then deleting the old ones *(p. 284)*
### 9.2 Performing an automatic rolling update with a ReplicationController *(p. 286)*
#### 9.2.1 Running the initial version of the app *(p. 286)*
#### 9.2.2 Performing a rolling update with kubectl *(p. 288)*
#### 9.2.3 Understanding why kubectl rolling-update is now obsolete *(p. 292)*
### 9.3 Using Deployments for updating apps declaratively *(p. 293)*
#### 9.3.1 Creating a Deployment *(p. 294)*
#### 9.3.2 Updating a Deployment *(p. 296)*
#### 9.3.3 Rolling back a deployment *(p. 300)*
#### 9.3.4 Controlling the rate of the rollout *(p. 303)*
#### 9.3.5 Pausing the rollout process *(p. 305)*
#### 9.3.6 Blocking rollouts of bad versions *(p. 306)*
### 9.4 Summary *(p. 311)*
## 10 StatefulSets: deploying replicated stateful applications *(p. 312)*
### 10.1 Replicating stateful pods *(p. 313)*
#### 10.1.1 Running multiple replicas with separate storage for each *(p. 313)*
#### 10.1.2 Providing a stable identity for each pod *(p. 314)*
### 10.2 Understanding StatefulSets *(p. 316)*
#### 10.2.1 Comparing StatefulSets with ReplicaSets *(p. 316)*
#### 10.2.2 Providing a stable network identity *(p. 317)*
#### 10.2.3 Providing stable dedicated storage to each stateful instance *(p. 319)*
#### 10.2.4 Understanding StatefulSet guarantees *(p. 321)*
### 10.3 Using a StatefulSet *(p. 322)*
#### 10.3.1 Creating the app and container image *(p. 322)*
#### 10.3.2 Deploying the app through a StatefulSet *(p. 323)*
#### 10.3.3 Playing with your pods *(p. 327)*
### 10.4 Discovering peers in a StatefulSet *(p. 331)*
#### 10.4.1 Implementing peer discovery through DNS *(p. 333)*
#### 10.4.2 Updating a StatefulSet *(p. 334)*
#### 10.4.3 Trying out your clustered data store *(p. 335)*
### 10.5 Understanding how StatefulSets deal with node failures *(p. 336)*
#### 10.5.1 Simulating a node’s disconnection from the network *(p. 336)*
#### 10.5.2 Deleting the pod manually *(p. 338)*
### 10.6 Summary *(p. 339)*
# Part 3 Beyond the basics *(p. 341)*
## 11 Understanding Kubernetes internals *(p. 341)*
### 11.1 Understanding the architecture *(p. 342)*
#### 11.1.1 The distributed nature of Kubernetes components *(p. 342)*
#### 11.1.2 How Kubernetes uses etcd *(p. 344)*
#### 11.1.3 What the API server does *(p. 348)*
#### 11.1.4 Understanding how the API server notifies clients of resource changes *(p. 350)*
#### 11.1.5 Understanding the Scheduler *(p. 351)*
#### 11.1.6 Introducing the controllers running in the Controller Manager *(p. 353)*
#### 11.1.7 What the Kubelet does *(p. 358)*
#### 11.1.8 The role of the Kubernetes Service Proxy *(p. 359)*
#### 11.1.9 Introducing Kubernetes add-ons *(p. 360)*
#### 11.1.10 Bringing it all together *(p. 362)*
### 11.2 How controllers cooperate *(p. 362)*
#### 11.2.1 Understanding which components are involved *(p. 362)*
#### 11.2.2 The chain of events *(p. 363)*
#### 11.2.3 Observing cluster events *(p. 364)*
### 11.3 Understanding what a running pod is *(p. 365)*
### 11.4 Inter-pod networking *(p. 367)*
#### 11.4.1 What the network must be like *(p. 367)*
#### 11.4.2 Diving deeper into how networking works *(p. 368)*
#### 11.4.3 Introducing the Container Network Interface *(p. 370)*
### 11.5 How services are implemented *(p. 370)*
#### 11.5.1 Introducing the kube-proxy *(p. 371)*
#### 11.5.2 How kube-proxy uses iptables *(p. 371)*
### 11.6 Running highly available clusters *(p. 373)*
#### 11.6.1 Making your apps highly available *(p. 373)*
#### 11.6.2 Making Kubernetes Control Plane components highly available *(p. 374)*
### 11.7 Summary *(p. 377)*
## 12 Securing the Kubernetes API server *(p. 378)*
### 12.1 Understanding authentication *(p. 378)*
#### 12.1.1 Users and groups *(p. 379)*
#### 12.1.2 Introducing ServiceAccounts *(p. 380)*
#### 12.1.3 Creating ServiceAccounts *(p. 381)*
#### 12.1.4 Assigning a ServiceAccount to a pod *(p. 383)*
### 12.2 Securing the cluster with role-based access control *(p. 385)*
#### 12.2.1 Introducing the RBAC authorization plugin *(p. 385)*
#### 12.2.2 Introducing RBAC resources *(p. 387)*
#### 12.2.3 Using Roles and RoleBindings *(p. 390)*
#### 12.2.4 Using ClusterRoles and ClusterRoleBindings *(p. 394)*
#### 12.2.5 Understanding default ClusterRoles and ClusterRoleBindings *(p. 403)*
#### 12.2.6 Granting authorization permissions wisely *(p. 405)*
### 12.3 Summary *(p. 405)*
## 13 Securing cluster nodes and the network *(p. 407)*
### 13.1 Using the host node’s namespaces in a pod *(p. 408)*
#### 13.1.1 Using the node’s network namespace in a pod *(p. 408)*
#### 13.1.2 Binding to a host port without using the host’s network namespace *(p. 409)*
#### 13.1.3 Using the node’s PID and IPC namespaces *(p. 411)*
### 13.2 Configuring the container’s security context *(p. 412)*
#### 13.2.1 Running a container as a specific user *(p. 413)*
#### 13.2.2 Preventing a container from running as root *(p. 414)*
#### 13.2.3 Running pods in privileged mode *(p. 414)*
#### 13.2.4 Adding individual kernel capabilities to a container *(p. 416)*
#### 13.2.5 Dropping capabilities from a container *(p. 417)*
#### 13.2.6 Preventing processes from writing to the container’s filesystem *(p. 418)*
#### 13.2.7 Sharing volumes when containers run as different users *(p. 419)*
### 13.3 Restricting the use of security-related features in pods *(p. 421)*
#### 13.3.1 Introducing the PodSecurityPolicy resource *(p. 421)*
#### 13.3.2 Understanding runAsUser, fsGroup, and supplementalGroups policies *(p. 424)*
#### 13.3.3 Configuring allowed, default, and disallowed capabilities *(p. 426)*
#### 13.3.4 Constraining the types of volumes pods can use *(p. 427)*
#### 13.3.5 Assigning different PodSecurityPolicies to different users and groups *(p. 428)*
### 13.4 Isolating the pod network *(p. 431)*
#### 13.4.1 Enabling network isolation in a namespace *(p. 431)*
#### 13.4.2 Allowing only some pods in the namespace to connect to a server pod *(p. 432)*
#### 13.4.3 Isolating the network between Kubernetes namespaces *(p. 433)*
#### 13.4.4 Isolating using CIDR notation *(p. 434)*
#### 13.4.5 Limiting the outbound traffic of a set of pods *(p. 435)*
### 13.5 Summary *(p. 435)*
## 14 Managing pods’ computational resources *(p. 436)*
### 14.1 Requesting resources for a pod’s containers *(p. 437)*
#### 14.1.1 Creating pods with resource requests *(p. 437)*
#### 14.1.2 Understanding how resource requests affect scheduling *(p. 438)*
#### 14.1.3 Understanding how CPU requests affect CPU time sharing *(p. 443)*
#### 14.1.4 Defining and requesting custom resources *(p. 443)*
### 14.2 Limiting resources available to a container *(p. 444)*
#### 14.2.1 Setting a hard limit for the amount of resources a container can use *(p. 444)*
#### 14.2.2 Exceeding the limits *(p. 446)*
#### 14.2.3 Understanding how apps in containers see limits *(p. 447)*
### 14.3 Understanding pod QoS classes *(p. 449)*
#### 14.3.1 Defining the QoS class for a pod *(p. 449)*
#### 14.3.2 Understanding which process gets killed when memory is low *(p. 452)*
### 14.4 Setting default requests and limits for pods per namespace *(p. 453)*
#### 14.4.1 Introducing the LimitRange resource *(p. 453)*
#### 14.4.2 Creating a LimitRange object *(p. 454)*
#### 14.4.3 Enforcing the limits *(p. 455)*
#### 14.4.4 Applying default resource requests and limits *(p. 456)*
### 14.5 Limiting the total resources available in a namespace *(p. 457)*
#### 14.5.1 Introducing the ResourceQuota object *(p. 457)*
#### 14.5.2 Specifying a quota for persistent storage *(p. 459)*
#### 14.5.3 Limiting the number of objects that can be created *(p. 459)*
#### 14.5.4 Specifying quotas for specific pod states and/or QoS classes *(p. 461)*
### 14.6 Monitoring pod resource usage *(p. 462)*
#### 14.6.1 Collecting and retrieving actual resource usages *(p. 462)*
#### 14.6.2 Storing and analyzing historical resource consumption statistics *(p. 464)*
### 14.7 Summary *(p. 467)*
## 15 Automatic scaling of pods and cluster nodes *(p. 469)*
### 15.1 Horizontal pod autoscaling *(p. 470)*
#### 15.1.1 Understanding the autoscaling process *(p. 470)*
#### 15.1.2 Scaling based on CPU utilization *(p. 473)*
#### 15.1.3 Scaling based on memory consumption *(p. 480)*
#### 15.1.4 Scaling based on other and custom metrics *(p. 480)*
#### 15.1.5 Determining which metrics are appropriate for autoscaling *(p. 482)*
#### 15.1.6 Scaling down to zero replicas *(p. 482)*
### 15.2 Vertical pod autoscaling *(p. 483)*
#### 15.2.1 Automatically configuring resource requests *(p. 483)*
#### 15.2.2 Modifying resource requests while a pod is running *(p. 483)*
### 15.3 Horizontal scaling of cluster nodes *(p. 484)*
#### 15.3.1 Introducing the Cluster Autoscaler *(p. 484)*
#### 15.3.2 Enabling the Cluster Autoscaler *(p. 486)*
#### 15.3.3 Limiting service disruption during cluster scale-down *(p. 486)*
### 15.4 Summary *(p. 488)*
## 16 Advanced scheduling *(p. 489)*
### 16.1 Using taints and tolerations to repel pods from certain nodes *(p. 489)*
#### 16.1.1 Introducing taints and tolerations *(p. 490)*
#### 16.1.2 Adding custom taints to a node *(p. 492)*
#### 16.1.3 Adding tolerations to pods *(p. 492)*
#### 16.1.4 Understanding what taints and tolerations can be used for *(p. 493)*
### 16.2 Using node affinity to attract pods to certain nodes *(p. 494)*
#### 16.2.1 Specifying hard node affinity rules *(p. 495)*
#### 16.2.2 Prioritizing nodes when scheduling a pod *(p. 497)*
### 16.3 Co-locating pods with pod affinity and anti-affinity *(p. 500)*
#### 16.3.1 Using inter-pod affinity to deploy pods on the same node *(p. 500)*
#### 16.3.2 Deploying pods in the same rack, availability zone, or geographic region *(p. 503)*
#### 16.3.3 Expressing pod affinity preferences instead of hard requirements *(p. 504)*
#### 16.3.4 Scheduling pods away from each other with pod anti-affinity *(p. 506)*
### 16.4 Summary *(p. 508)*
## 17 Best practices for developing apps *(p. 509)*
### 17.1 Bringing everything together *(p. 510)*
### 17.2 Understanding the pod’s lifecycle *(p. 511)*
#### 17.2.1 Applications must expect to be killed and relocated *(p. 511)*
#### 17.2.2 Rescheduling of dead or partially dead pods *(p. 514)*
#### 17.2.3 Starting pods in a specific order *(p. 515)*
#### 17.2.4 Adding lifecycle hooks *(p. 517)*
#### 17.2.5 Understanding pod shutdown *(p. 521)*
### 17.3 Ensuring all client requests are handled properly *(p. 524)*
#### 17.3.1 Preventing broken client connections when a pod is starting up *(p. 524)*
#### 17.3.2 Preventing broken connections during pod shut-down *(p. 525)*
### 17.4 Making your apps easy to run and manage in Kubernetes *(p. 529)*
#### 17.4.1 Making manageable container images *(p. 529)*
#### 17.4.2 Properly tagging your images and using imagePullPolicy wisely *(p. 529)*
#### 17.4.3 Using multi-dimensional instead of single-dimensional labels *(p. 530)*
#### 17.4.4 Describing each resource through annotations *(p. 530)*
#### 17.4.5 Providing information on why the process terminated *(p. 530)*
#### 17.4.6 Handling application logs *(p. 532)*
### 17.5 Best practices for development and testing *(p. 534)*
#### 17.5.1 Running apps outside of Kubernetes during development *(p. 534)*
#### 17.5.2 Using Minikube in development *(p. 535)*
#### 17.5.3 Versioning and auto-deploying resource manifests *(p. 536)*
#### 17.5.4 Introducing Ksonnet as an alternative to writing YAML/JSON manifests *(p. 537)*
#### 17.5.5 Employing Continuous Integration and Continuous Delivery (CI/CD) *(p. 538)*
### 17.6 Summary *(p. 538)*
## 18 Extending Kubernetes *(p. 540)*
### 18.1 Defining custom API objects *(p. 540)*
#### 18.1.1 Introducing CustomResourceDefinitions *(p. 541)*
#### 18.1.2 Automating custom resources with custom controllers *(p. 545)*
#### 18.1.3 Validating custom objects *(p. 549)*
#### 18.1.4 Providing a custom API server for your custom objects *(p. 550)*
### 18.2 Extending Kubernetes with the Kubernetes Service Catalog *(p. 551)*
#### 18.2.1 Introducing the Service Catalog *(p. 552)*
#### 18.2.2 Introducing the Service Catalog API server and Controller Manager *(p. 553)*
#### 18.2.3 Introducing Service Brokers and the OpenServiceBroker API *(p. 554)*
#### 18.2.4 Provisioning and using a service *(p. 556)*
#### 18.2.5 Unbinding and deprovisioning *(p. 558)*
#### 18.2.6 Understanding what the Service Catalog brings *(p. 558)*
### 18.3 Platforms built on top of Kubernetes *(p. 559)*
#### 18.3.1 Red Hat OpenShift Container Platform *(p. 559)*
#### 18.3.2 Deis Workflow and Helm *(p. 562)*
### 18.4 Summary *(p. 565)*
# Appendix A—Using kubectl with multiple clusters *(p. 566)*
## A.1 Switching between Minikube and Google Kubernetes Engine *(p. 566)*
## A.2 Using kubectl with multiple clusters or namespaces *(p. 567)*
### A.2.1 Configuring the location of the kubeconfig file *(p. 567)*
### A.2.2 Understanding the contents of the kubeconfig file *(p. 567)*
### A.2.3 Listing, adding, and modifying kube config entries *(p. 568)*
### A.2.4 Using kubectl with different clusters, users, and contexts *(p. 569)*
### A.2.5 Switching between contexts *(p. 570)*
### A.2.6 Listing contexts and clusters *(p. 570)*
### A.2.7 Deleting contexts and clusters *(p. 570)*
# Appendix B—Setting up a multi-node cluster with kubeadm *(p. 571)*
## B.1 Setting up the OS and required packages *(p. 571)*
### B.1.1 Creating the virtual machine *(p. 571)*
### B.1.2 Configuring the network adapter for the VM *(p. 572)*
### B.1.3 Installing the operating system *(p. 573)*
### B.1.4 Installing Docker and Kubernetes *(p. 576)*
### B.1.5 Cloning the VM *(p. 577)*
## B.2 Configuring the master with kubeadm *(p. 579)*
### B.2.1 Understanding how kubeadm runs the components *(p. 580)*
## B.3 Configuring worker nodes with kubeadm *(p. 581)*
### B.3.1 Setting up the container network *(p. 582)*
## B.4 Using the cluster from your local machine *(p. 582)*
# Appendix C—Using other container runtimes *(p. 584)*
## C.1 Replacing Docker with rkt *(p. 584)*
### C.1.1 Configuring Kubernetes to use rkt *(p. 584)*
### C.1.2 Trying out rkt with Minikube *(p. 585)*
## C.2 Using other container runtimes through the CRI *(p. 587)*
### C.2.1 Introducing the CRI-O Container Runtime *(p. 587)*
### C.2.2 Running apps in virtual machines instead of containers *(p. 587)*
# Appendix D—Cluster Federation *(p. 588)*
## D.1 Introducing Kubernetes Cluster Federation *(p. 588)*
## D.2 Understanding the architecture *(p. 589)*
## D.3 Understanding federated API objects *(p. 590)*
### D.3.1 Introducing federated versions of Kubernetes resources *(p. 590)*
### D.3.2 Understanding what federated resources do *(p. 591)*
# index *(p. 593)*
## Symbols *(p. 593)*
## Numerics *(p. 593)*
## A *(p. 593)*
## B *(p. 595)*
## C *(p. 595)*
## D *(p. 600)*
## E *(p. 603)*
## F *(p. 604)*
## G *(p. 604)*
## H *(p. 605)*
## I *(p. 605)*
## J *(p. 606)*
## K *(p. 606)*
## L *(p. 608)*
## M *(p. 609)*
## N *(p. 610)*
## O *(p. 612)*
## P *(p. 612)*
## Q *(p. 616)*
## R *(p. 617)*
## S *(p. 620)*
## T *(p. 624)*
## U *(p. 625)*
## V *(p. 625)*
## W *(p. 626)*
## X *(p. 626)*
## Y *(p. 626)*
# Kubernetes in Action–back *(p. 628)*