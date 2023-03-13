# Binance

Folder **src/** : python script that get datas, and make graph from those data

Folder **data/** : graphics in png formats stored into folders

To launch programs : 
``` start.sh ```: it will launch all the programs

```start.sh v ```: to get wallet value diagram.

```start.sh r ```: to get wallet repartition diagram.

```start.sh d ```: to get all deposits diagram.

```start.sh b ```: to get bitcoin value diagram.

There are also programs to get actual wallet value, all deposits/withdrawals value ...


BUT, to run this programs, you need to have a Binance account, and create a folder **credentials** at the folder root, with a file **key_store.json**. 
This file must be of the following format : 
{
  "api_key" : <your_key>,
  "secret_key": <your_secret_key>
}
If those rules are not respected, the programs will not run.
