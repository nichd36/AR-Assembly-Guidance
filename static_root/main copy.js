let APP_ID = "c3b064f2e4274ca09c3e6a4c7f4b9b3b"

let token = null; //as now only testing, use app id only

let uid = String(Math.floor(Math.random()*10000)) //ltr change to emp_id

let client;
let channel;

let localStream;
let remoteStream;
let peerConnection;

const servers = {
        iceServers:[
                {
                        urls:['stun:stun.l.google.com:19302', 'stun:stun1.l.google.com:19302']
                }
        ]
} 

let init = async () => {
        client = await AgoraRTM.createInstance(APP_ID)
        await client.login({uid, token})

        //index.html?room=232323
        channel = client.createChannel('main')
        await channel.join()

        channel.on('MemberJoined', handleUserJoined)

        localStream = await navigator.mediaDevices.getUserMedia({video:true, audio:false})
        document.getElementById('user-1').srcObject = localStream

        createOffer()
}

let handleUserJoined = async (MemberId) => {
        console.log("A new user joined the channel: ", MemberId)
}

let createOffer = async () => {
        peerConnection = new RTCPeerConnection(servers)

        remoteStream = new MediaStream()
        document.getElementById('user-2').srcObject = remoteStream

        localStream.getTracks().forEach((track) => {
                peerConnection.addTrack(track, localStream)
        })

        peerConnection.ontrack = (event) => {
                event.streams[0].getTracks.forEach((track) => {
                        remoteStream.addTrack(track)
                })
        }

        peerConnection.onicecandidate = async (event) => {
                if(event.candidate){
                        console.log("NEW ice candidate: ", event.candidate)
                }
        }

        let offer = await peerConnection.createOffer()
        await peerConnection.setLocalDescription(offer)
        
        console.log('Offer: ', offer)
}

init()
