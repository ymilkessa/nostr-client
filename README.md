# Nostr client with python

This is a simple console-based implementation of a Nostr-client. It supports creation of valid user keys, posting text to relays, fetching posts from other users, and adding new relays. The user keys that get created are saved with a password-protected encryption.

Everything implemented here is based on [this page](https://github.com/nostr-protocol/nips/blob/master/01.md).

## How to run the client

#### Prerequisites:

- Python3
- Pipenv

First clone this repo and inside the main folder run:

```
$ pipenv install
$ python src/client_manager.py
```

This should start the dialog in the console. You should be first prompted to create a password with which to encrypt your keys on your machine.

## Usage

I have already added a short list of relays in [this file](https://github.com/ymilkessa/nostr-client/blob/main/myrelays).

- Enter `i` to view your public key. To view your private key, enter `i --all` or `i -a`.
- Enter `p` to post content to all the relays. You will then be prompted to enter the text to be posted.
- Enter `s` to fetch content posted by another user. This will prompt you to enter the public key of this other user.
- Enter `a` to add new relay addresses.
- Enter `e` to exit.
- `h` just shows the list of commands.
