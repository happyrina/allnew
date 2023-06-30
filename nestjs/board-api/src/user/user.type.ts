export type Login = {
    email : string;
    password : string;
}

export type Resiter = {
    email : string;
    name : string;
    password : string;
}

export type UserInfo = {
    uuid : string;
    email : string;
    name : string;
}

export type LoginUserInfo = {
    uuid : string;
    email : string;
    name : string;
    lastLogin : string;
}