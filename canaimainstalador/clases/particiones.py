#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import parted, _ped

from canaimainstalador.clases.common import ProcessGenerator, espacio_usado
from canaimainstalador.config import *

class Particiones():
    def __init__(self):
        pass

    def nueva_tabla_particiones(self, drive, t):
        dev = parted.Device(drive)
        new = parted.freshDisk(dev, t)
        try:
            new.commit()
        except _ped.IOException as x:
            print x

    def lista_discos(self):
        '''
            devuelve los discos que están conectados al equipo
        '''
        l = []
        dev = parted.getAllDevices()
        for d in dev:
            l.append(d.path)
        return sorted(l)

    def lista_particiones(self, disco):
        '''
            Crea una lista de particiones disponibles en un disco dado
        '''
        l = []
        p = []

        try:
            dev = parted.Device(disco)
            disk = parted.Disk(dev)
        except _ped.DiskLabelException:
            return p

        sectorsize = dev.sectorSize
        total = float(dev.getSize(unit='KB'))

        for j in disk.partitions:
            l.append(j)

        for w in disk.getFreeSpacePartitions():
            l.append(w)

        for i in l:
            code = i.type
            part = i.path
            ini = float(i.geometry.start * sectorsize / 1024)
            fin = float(i.geometry.end * sectorsize / 1024)
            tam = float(i.geometry.length * sectorsize / 1024)
            num = int(i.number)
            usado = tam
            libre = float(0)

            if num != -1:
                if i.fileSystem != None:
                    if code != 2:
                        if i.fileSystem.type == 'linux-swap(v1)':
                            fs = 'swap'
                            usado = tam
                            libre = float(0)
                        else:
                            fs = i.fileSystem.type
                            usado = espacio_usado(fs, part)
                            libre = tam - usado
                else:
                    if code == 2:
                        fs = 'extended'
                    else:
                        fs = 'unknown'
                flags = i.getFlagsAsString()
            else:
                fs = 'free'
                libre = tam
                usado = float(0)
                flags = ''

            if not flags:
                flags = 'none'

            if libre < 0 or usado == 'unknown':
                libre = float(0)
                usado = tam

            if code == 0 or code == 4:
                tipo = 'primary'
            elif code == 1 or code == 5:
                tipo = 'logical'
            elif code == 2:
                tipo = 'extended'

            p.append(
                [part, ini, fin, tam, fs, tipo, flags, usado, libre, total, num]
                )

        return sorted(p, key=lambda particiones: particiones[1])

    def nombre_particion(self, drive, start, end):

        dev = parted.Device(drive)
        disk = parted.Disk(dev)
        s_sec = start * 1024 / dev.sectorSize
        e_sec = end * 1024 / dev.sectorSize
        m_sec = ((e_sec - s_sec) / 2) + s_sec
        return disk.getPartitionBySector(m_sec).path

    def crear_particion(self, drive, start, end, fs, partype):
        '''
        Argumentos:
        - disco: el disco donde se realizará la partición. Ej: /dev/sda
        - tipo: el tipo de partición a realizar {primary, extended, logical}
        - formato: el formato que usará la partición {ext2, ext4, linux-swap,fat32, ntfs}
        - inicio: donde comenzará la partición, en kB
        - fin: donde terminará la partición, en kB
        '''
        i = 0
        dev = parted.Device(drive)
        disk = parted.Disk(dev)
        s_sec = start * 1024 / dev.sectorSize
        e_sec = end * 1024 / dev.sectorSize

        if partype == 'primary' or partype == 0:
            partype = _ped.PARTITION_NORMAL
        elif partype == 'logical' or partype == 1:
            partype = _ped.PARTITION_LOGICAL
        elif partype == 'extended' or partype == 2:
            partype = _ped.PARTITION_EXTENDED
        else:
            return False

        try:
            geometry = parted.Geometry(device=dev, start=s_sec, end=e_sec)
            i += 1
        except Exception as a:
            print a

        try:
            constraint = parted.Constraint(exactGeom=geometry)
            i += 1
        except Exception as b:
            print b

        try:
            partition = parted.Partition(disk=disk, type=partype, geometry=geometry)
            i += 1
        except Exception as c:
            print c

        try:
            disk.addPartition(partition=partition, constraint=constraint)
            i += 1
        except Exception as d:
            print d

        try:
            disk.commit()
            i += 1
        except Exception as e:
            print e

        if i == 5:
            if partype == _ped.PARTITION_EXTENDED:
                return True
            else:
                if fs in FSPROGS:
                    ProcessGenerator(
                        FSPROGS[fs][0].format(self.nombre_particion(drive, start, end))
                        )
                return True
        else:
            return False

    def formatear_particion(self, part, fs):
        '''
        Argumentos:
        - disco: el disco donde se realizará la partición. Ej: /dev/sda
        - tipo: el tipo de partición a realizar {primary, extended, logical}
        - formato: el formato que usará la partición {ext2, ext4, linux-swap,fat32, ntfs}
        - inicio: donde comenzará la partición, en kB
        - fin: donde terminará la partición, en kB
        '''
        if fs in FSPROGS:
            ProcessGenerator(FSPROGS[fs][0].format(part))
            return True
        else:
            return False

    def borrar_particion(self, part):
        '''
        Argumentos:
        - disco: el disco donde se realizará la partición. Ej: /dev/sda
        - tipo: el tipo de partición a realizar {primary, extended, logical}
        - formato: el formato que usará la partición {ext2, ext4, linux-swap,fat32, ntfs}
        - inicio: donde comenzará la partición, en kB
        - fin: donde terminará la partición, en kB
        '''
        i = 0
        dev = parted.Device(part[:-1])
        disk = parted.Disk(dev)
        partition = disk.getPartitionByPath(part)

        try:
            disk.deletePartition(partition=partition)
            i += 1
        except Exception as x:
            print x

        try:
            disk.commit()
            i += 1
        except Exception as y:
            print y

        if i == 2:
            return True
        else:
            return False

    def redimensionar_particion(self, part, newend):
        '''
        Argumentos:
        - disco: el disco donde se realizará la partición. Ej: /dev/sda
        - tipo: el tipo de partición a realizar {primary, extended, logical}
        - formato: el formato que usará la partición {ext2, ext4, linux-swap,fat32, ntfs}
        - inicio: donde comenzará la partición, en kB
        - fin: donde terminará la partición, en kB
        '''
        drive = part[:-1]
        dev = parted.Device(drive)
        disk = parted.Disk(dev)
        partition = disk.getPartitionByPath(part)
        fs = partition.fileSystem.type
        partype = partition.type
        currstart = partition.geometry.start * dev.sectorSize / 1024
        currend = partition.geometry.end * dev.sectorSize / 1024
        newsize = str(int((newend - currstart))) + 'K'

        if newend > currend:
            # Redimensionar primero la partición y luego el sistema de archivos
            if self.borrar_particion(part=part):
                if fs == 'linux-swap(v1)':
                    if self.crear_particion(
                        drive=drive, start=currstart, end=newend,
                        fs='swap', partype=partype
                        ):
                        return True
                else:
                    if self.crear_particion(
                        drive=drive, start=currstart, end=newend,
                        fs=None, partype=partype
                        ):
                        if FSPROGS[fs][1] != '':
                            if fs == 'btrfs':
                                ProcessGenerator('umount /mnt')
                                ProcessGenerator('mount {0} /mnt'.format(part))
                            if ProcessGenerator(
                                FSPROGS[fs][1].format(newsize, part)
                                ).returncode == 0:
                                if fs == 'btrfs':
                                    ProcessGenerator('umount /mnt')
                                return True
                        else:
                            return False
        elif newend < currend:
            # Redimensionar primero el sistema de archivos y luego la partición
            if fs == 'linux-swap(v1)':
                if self.borrar_particion(part=part):
                    if self.crear_particion(
                        drive=drive, start=currstart, end=newend,
                        fs='swap', partype=partype
                        ):
                        return True
            else:
                if FSPROGS[fs][1] != '':
                    if fs == 'btrfs':
                        ProcessGenerator('umount /mnt')
                        ProcessGenerator('mount {0} /mnt'.format(part))
                        ProcessGenerator(FSPROGS[fs][1].format(newsize, part))
                        ProcessGenerator('umount /mnt')
                    else:
                        ProcessGenerator(FSPROGS[fs][1].format(newsize, part))

                    if self.borrar_particion(part=part):
                        if self.crear_particion(
                            drive=drive, start=currstart, end=newend,
                            fs=None, partype=partype
                            ):
                            return True
                else:
                    return False

        elif newend == currend:
            return True
