# Café-Messenger

[![Gitter](https://badges.gitter.im/Join%20Chat.svg)](https://gitter.im/PhasecoreX/Caf-Messenger?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)

A Python 2.7 instant messenger for encrypted communication between decentralized peers.

In no way is this project complete. It has been moved here from BitBucket in hopes that it may be helpful to others, or that it can someday be finished.

## Features
* Uses RSA for peer identification
* Uses AES for message encryption
* Uses Kademlia for creating a distributed network of peers

## Dependencies
* Python 2.7
* PyCrypto
* Twisted
* [Kademlia](https://github.com/bmuller/kademlia) (pip install kademlia)

## Future Goals
This project was for a capstone class at Grand Valley State University. The team had more plans for the project, but never got around to doing them. Below are some of those goals:
* Separate GUI from backend
* Refactor to Pep8 standards
* Actually get Kademlia to work correctly
