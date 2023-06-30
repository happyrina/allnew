import { Entity, PrimaryGeneratedColumn, Column, CreateDateColumn, UpdateDateColumn } from "typeorm";

@Entity({name:"user", schema:"board"})
export class User {
    @PrimaryGeneratedColumn({
        name: "user_id"
    })
    id : number;
    
    @Column({length: 40})
    uuid : string;
    
    @Column({length: 20})
    name : string;
    
    @Column({length: 100})
    email : string;
    
    @Column({length: 100})
    password : string;
    
    @Column("datetime", {
        name : "last_login_date"
    })
    lastLoginDate : Date;

    @Column({
        name : "created_at"
    })
    createDate : Date;
    
    @UpdateDateColumn({
        name : "updated_at"
    })
    updateDate : Date;
}