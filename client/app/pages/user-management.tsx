import { getUsers } from "~/api/users";
import type { Route } from "./+types/user-management";

import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "~/components/ui/table";
import { Avatar, AvatarFallback, AvatarImage } from "~/components/ui/avatar";
import { format, parseISO } from "date-fns";

export async function loader({}) {
  return await getUsers();
}

export async function clientLoader({}) {
  return await getUsers();
}

export default function UserManagementPage({
  loaderData,
}: Route.ComponentProps) {
  const users = loaderData;

  return (
    <Table>
      <TableHeader>
        <TableRow>
          <TableHead>Full name</TableHead>
          <TableHead>Joined date</TableHead>
        </TableRow>
      </TableHeader>
      <TableBody>
        {users.map((user) => (
          <TableRow key={user.id}>
            <TableCell className="flex flex-row items-center gap-4">
              <Avatar>
                {user.avatarUrl && <AvatarImage src={user.avatarUrl} />}
                <AvatarFallback>
                  {user?.name?.match(/\b\w/g)?.join("").toUpperCase()}
                </AvatarFallback>
              </Avatar>
              {user.name}
            </TableCell>
            <TableCell>
              {user.createdAt &&
                format(parseISO(user.createdAt), "MMMM d, yyyy")}
            </TableCell>
          </TableRow>
        ))}
      </TableBody>
    </Table>
  );
}
